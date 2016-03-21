"""models.py - This file contains the class definitions for the Datastore
entities used by the Game. Because these classes are also regular Python
classes they can include methods (such as 'to_form' and 'new_game')."""

from protorpc import messages
from google.appengine.ext import ndb


class User(ndb.Model):
    """User profile"""
    name = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)

class Game(ndb.Model):
    """Game between two players including multiple Matches"""
    player_1_name = ndb.StringProperty()
    player_2_name = ndb.StringProperty()

class Match(ndb.Model):
    """Match (in Game)"""
    player_1_name = ndb.StringProperty()
    player_2_name = ndb.StringProperty()
    player_1_entry = ndb.BooleanProperty()
    player_2_entry = ndb.BooleanProperty()
    is_active = ndb.BooleanProperty()
    start_time = ndb.DateTimeProperty()

class StringMessage(messages.Message):
    """StringMessage-- outbound (single) string message"""
    message = messages.StringField(1, required=True)
