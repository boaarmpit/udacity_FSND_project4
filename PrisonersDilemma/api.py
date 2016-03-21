"""api.py - Create and configure the Game API exposing the resources.
This can also contain game logic. For more complex games it would be wise to
move game logic to another file. Ideally the API will be simple, concerned
primarily with communication to/from the API's users."""

from datetime import datetime
import endpoints
from protorpc import remote, messages
from google.appengine.api import oauth

from models import User, Game, Match
from models import StringMessage
from utils import get_by_urlsafe

USER_REQUEST = endpoints.ResourceContainer(
    user_name=messages.StringField(1))

GAME_REQUEST = endpoints.ResourceContainer(
    player_1_name=messages.StringField(1),
    player_2_name=messages.StringField(2))

CREATE_MATCH_REQUEST = endpoints.ResourceContainer(
    player_1_name=messages.StringField(1),
    player_2_name=messages.StringField(2))

CREATE_GAME_REQUEST = endpoints.ResourceContainer(
    match_key=messages.StringField(1))

GET_GAME_REQUEST = endpoints.ResourceContainer(
    game_key=messages.StringField(1))

PLAY_GAME_REQUEST = endpoints.ResourceContainer(
    game_key=messages.StringField(1),
    player_name=messages.StringField(2),
    play=messages.BooleanField(3))

@endpoints.api(name='prisoner', version='v1')
class PrisonerApi(remote.Service):
    """Game API"""
    @endpoints.method(request_message=USER_REQUEST,
                      response_message=StringMessage,
                      path='create_user',
                      name='create_user',
                      http_method='POST')
    def create_user(self, request):
        """Create a User. Requires a unique username.
        Gets email from oauth account"""
        scope = 'https://www.googleapis.com/auth/userinfo.email'
        user = oauth.get_current_user(scope)

        if User.query(User.name == request.user_name).get():
            raise endpoints.ConflictException(
                'A User with that name already exists!')
        user = User(name=request.user_name, email=user.email(), score=0)
        user.put()
        return StringMessage(message='User {} created!'.format(
                request.user_name))

    @endpoints.method(request_message=CREATE_MATCH_REQUEST,
                      response_message=StringMessage,
                      path='create_match',
                      name='create_match',
                      http_method='POST')
    def create_match(self, request):
        """Create a Match between two Users"""

        if request.player_1_name == request.player_2_name:
            raise endpoints.ConflictException(
                'Cannot create a match between a player and themselves!')
        for player_name in [request.player_1_name, request.player_2_name]:
            if not User.query(User.name == player_name).get():
                raise endpoints.ConflictException(
                    'No user named {} exists!'.format(player_name))

        match = Match(player_1_name=request.player_1_name,
                      player_2_name=request.player_2_name)

        match_key = match.put()
        return StringMessage(message='Match created between {} and {}! '
                                     '(key={})'.format(request.player_1_name,
                                                       request.player_2_name,
                                                       match_key.urlsafe()))

    @endpoints.method(request_message=CREATE_GAME_REQUEST,
                      response_message=StringMessage,
                      path='create_game',
                      name='create_game',
                      http_method='POST')
    def create_game(self, request):
        """Create a Game between two Users"""

        match = get_by_urlsafe(request.match_key, Match)
        if not match:
            raise endpoints.ConflictException('Cannot find match with key {}'.
                                              format(request.match_key))

        game = Game(parent=match.key,
                    start_time=datetime.now())

        game_key = game.put()
        return StringMessage(message='Game created between {} and {}! '
                                     '(key={})'.format(match.player_1_name,
                                                       match.player_2_name,
                                                       game_key.urlsafe()))

    @endpoints.method(request_message=GET_GAME_REQUEST,
                      response_message=StringMessage,
                      path='get_game',
                      name='get_game',
                      http_method='POST')
    def get_game(self, request):
        """Get a Game from its websafe key"""

        game = get_by_urlsafe(request.game_key, Game)
        if not game:
            raise endpoints.ConflictException('Cannot find game with key {}'.
                                              format(request.game_key))
        match = game.key.parent().get()

        return StringMessage(message='Found game between {} and {} with key {}'
                                     ''.format(match.player_1_name,
                                               match.player_2_name,
                                               request.game_key))

    @endpoints.method(request_message=PLAY_GAME_REQUEST,
                      response_message=StringMessage,
                      path='play_game',
                      name='play_game',
                      http_method='POST')
    def play_game(self, request):
        """Play move in a Game"""

        game = get_by_urlsafe(request.game_key, Game)
        if not game:
            raise endpoints.ConflictException('Cannot find game with key {}'.
                                              format(request.game_key))
        match = game.key.parent().get()

        if not User.query(User.name == request.player_name).get():
                raise endpoints.ConflictException(
                    'No user named {} exists!'.format(request.player_name))

        if match.player_1_name == request.player_name:
            game.player_1_entry = request.play
        elif match.player_2_name == request.player_name:
            game.player_2_entry = request.play
        else:
            raise endpoints.ConflictException('Player {} is not playing in '
                                              'game {}'.
                                              format(request.player_name,
                                                     request.game_key))
        game.put()

        result = 'Not all players have played yet'
        if game.player_1_entry is not None \
                and game.player_2_entry is not None:
            if game.player_1_entry:
                if game.player_2_entry:
                    p1_score, p2_score = 2, 2
                else:
                    p1_score, p2_score = 0, 3
            else:
                if game.player_2_entry:
                    p1_score, p2_score = 3, 0
                else:
                    p1_score, p2_score = 1, 1
            result = 'Result: {}:{} years, {}:{} years.'.format(
                match.player_1_name, p1_score, match.player_2_name, p2_score)

        return StringMessage(message='Registered player {}\'s play of {} in '
                                     'game {} . '.format(request.player_name,
                                                       request.play,
                                                       request.game_key)
                                     +result)

api = endpoints.api_server([PrisonerApi])