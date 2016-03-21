"""models.py - This file contains the class definitions for the Datastore
entities used by the Game. Because these classes are also regular Python
classes they can include methods (such as 'to_form' and 'new_game')."""

from protorpc import messages
from google.appengine.ext import ndb


class User(ndb.Model):
    """User profile"""
    name = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    score = ndb.IntegerProperty(required=True)  # Number of wins minus losses

class Match(ndb.Model):
    """Match between two players including multiple Games"""
    player_1_name = ndb.StringProperty()
    player_2_name = ndb.StringProperty()
    player_1_penalty = ndb.IntegerProperty()  # Penalty in years
    player_2_penalty = ndb.IntegerProperty()  # Penalty in years
    games_remaining = ndb.IntegerProperty()
    is_active = ndb.BooleanProperty()

class Game(ndb.Model):
    """Game (in Match)"""
    player_1_move = ndb.BooleanProperty()  # True corresponds to defecting
    player_2_move = ndb.BooleanProperty()  # True corresponds to defecting
    is_active = ndb.BooleanProperty()
    start_time = ndb.DateTimeProperty()

class StringMessage(messages.Message):
    """StringMessage-- outbound (single) string message"""
    message = messages.StringField(1, required=True)

class StringMessages(messages.Message):
    """StringMessage-- outbound (repeated) string message"""
    message = messages.StringField(1, repeated=True)