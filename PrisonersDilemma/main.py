#!/usr/bin/env python

"""main.py - This file contains handlers that are called by taskqueue and/or
cronjobs."""

import webapp2
from google.appengine.api import mail, app_identity
from google.appengine.ext import ndb
from models import User, Match


class SendReminderEmail(webapp2.RequestHandler):
    def get(self):
        """Send a reminder email to each User with active Matches.
        Called every hour using a cron job"""
        app_id = app_identity.get_application_id()
        users = User.query(User.email != None)

        for user in users:
            matches = Match.query(ndb.AND(Match.is_active == True,
                                          ndb.OR(
                                              Match.player_1_name == user.name,
                                              Match.player_2_name == user.name)
                                          )).fetch()

            if matches:
                subject = 'Unfinished match reminder!'
                body = 'Hello {}, \n\nThe following matches are still in ' \
                       'progress:\n'.format(user.name)
                html = 'Hello {}, <br><br>The following matches are still in ' \
                       'progress:<br>'.format(user.name)
                for match in matches:
                    body += '{} vs {}\n'.format(match.player_1_name,
                                                match.player_2_name)
                    html += '{} vs {}<br>'.format(match.player_1_name,
                                                  match.player_2_name)
                body += 'https://{}.appspot.com">Continue playing'\
                    .format(app_id)
                html += '<a href="https://{}.appspot.com">Continue playing' \
                        '</a>'.format(app_id)
                mail.send_mail('noreply@{}.appspotmail.com'.format(app_id),
                               user.email, subject, body, html=html)

app = webapp2.WSGIApplication([('/crons/send_reminder', SendReminderEmail)],
                              debug=True)
