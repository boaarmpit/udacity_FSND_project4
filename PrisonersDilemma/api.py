"""api.py - Create and configure the Game API exposing the resources.
This can also contain game logic. For more complex games it would be wise to
move game logic to another file. Ideally the API will be simple, concerned
primarily with communication to/from the API's users."""

from datetime import datetime
import endpoints
from protorpc import remote, messages
from google.appengine.api import oauth

from models import User, Match
from models import StringMessage
from utils import get_by_urlsafe

USER_REQUEST = endpoints.ResourceContainer(
    user_name=messages.StringField(1))

MATCH_REQUEST = endpoints.ResourceContainer(
    player_1_name=messages.StringField(1),
    player_2_name=messages.StringField(2))

GET_MATCH_REQUEST = endpoints.ResourceContainer(
    websafekey=messages.StringField(1))

PLAY_MATCH_REQUEST = endpoints.ResourceContainer(
    websafekey=messages.StringField(1),
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
        user = User(name=request.user_name, email=user.email())
        user.put()
        return StringMessage(message='User {} created!'.format(
                request.user_name))

    @endpoints.method(request_message=MATCH_REQUEST,
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
                      player_2_name=request.player_2_name,
                      start_time=datetime.now())
        match_key = match.put()
        return StringMessage(message='Match created between {} and {}! '
                                     '(key={})'.format(request.player_1_name,
                                                       request.player_2_name,
                                                       match_key.urlsafe()))

    @endpoints.method(request_message=GET_MATCH_REQUEST,
                      response_message=StringMessage,
                      path='get_match',
                      name='get_match',
                      http_method='POST')
    def get_match(self, request):
        """Get a Match from its websafe key"""

        match = get_by_urlsafe(request.websafekey, Match)
        if not match:
            raise endpoints.ConflictException('Cannot find match with key {}'.
                                              format(request.websafekey))

        return StringMessage(message='Found match between {} and {} with '
                                     'key {}'.format(match.player_1_name,
                                                     match.player_2_name,
                                                     request.websafekey))

    @endpoints.method(request_message=PLAY_MATCH_REQUEST,
                      response_message=StringMessage,
                      path='play_match',
                      name='play_match',
                      http_method='POST')
    def play_match(self, request):
        """Play move in a Match"""

        match = get_by_urlsafe(request.websafekey, Match)
        if not match:
            raise endpoints.ConflictException('Cannot find match with key {}'.
                                              format(request.websafekey))

        if not User.query(User.name == request.player_name).get():
                raise endpoints.ConflictException(
                    'No user named {} exists!'.format(request.player_name))

        if match.player_1_name == request.player_name:
            match.player_1_entry = request.play
        elif match.player_2_name == request.player_name:
            match.player_2_entry = request.play
        else:
            raise endpoints.ConflictException('Player {} is not playing in '
                                              'match {}'.
                                              format(request.player_name,
                                                     request.websafekey))
        match.put()
        return StringMessage(message='Registered player {}\'s play of {} in '
                                     'match {}'.format(request.player_name,
                                                       request.play,
                                                       request.websafekey))

api = endpoints.api_server([PrisonerApi])