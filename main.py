#!/usr/bin/env python
# coding: utf-8
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import string
import os
import cgi
import logging

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import *
from google.appengine.ext.db import djangoforms
from google.appengine.api import users
from google.appengine.api import mail
from google.appengine.api.labs import taskqueue

import meplist
import bodies

countrylist = sorted(meplist.meps.keys())

class SentMails(db.Model):
    """ Mapping of user to country for which MEPs mail was sent"""
    friend = db.UserProperty()
    country = db.StringProperty(choices = countrylist)

class SentMailsForm(djangoforms.ModelForm):
    class Meta:
        model = SentMails
        exclude = ['friend']

class MainHandler(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user == None:
            nick = "Not Signed in User"
        else:
            nick = user.nickname()
            nick = string.join(map(string.capitalize, string.split(nick)))

        template_values = {'username': nick, 'form': SentMailsForm(), 'meps': meplist.meps, 'bodies': bodies.bodies}
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))

mail_subj = "Declaration 54/2009"

class SendMail(webapp.RequestHandler):
    @login_required
    def get(self):
        user = users.get_current_user()
        user_address = user.email()
        user_name = self.request.str_GET["username"]
        country = self.request.str_GET["country"]

        query = SentMails.gql("WHERE friend = :1 AND country = :2", user, country)

        res = query.get()

        if res:
            self.redirect(users.create_logout_url('/done'))
            return

        #split Mr/Ms greeting from mail body
        body = bodies.bodies[country]
        bs = body.split('\n', 3)

        body = bs[3]

        if mail.is_email_valid(user_address):
            for mep in meplist.meps[country]:
                m, dest_address = mep.split()
                if m == "Mr":
                    greet = bs[1]
                else:
                    greet = bs[2]

                if True:
                    logging.info(dest_address)
                    mail.send_mail(user_address,
                        'jani.monoses@gmail.com',
                        mail_subj,
                        greet + body + user_name
                        )
                    break
                else:
                    mail.send_mail(user_address,
                        dest_address,
                        mail_subj,
                        greet + body + user_name
                        )

        # Save
        sm = SentMails()
        sm.friend = user
        sm.country = country
        sm.put()

        self.redirect(users.create_logout_url('/done?meps=%d' % (len(meplist.meps[country]))))

class SentMail(webapp.RequestHandler):
    def get(self):
        template_values = {'num': self.request.get('meps')}
        path = os.path.join(os.path.dirname(__file__), 'done.html')
        self.response.out.write(template.render(path, template_values))

def main():
    application = webapp.WSGIApplication([
        ('/', MainHandler),
        ('/mail', SendMail),
        ('/done', SentMail),
        ],
        debug=True)
    run_wsgi_app(application)


if __name__ == '__main__':
    main()

# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab

