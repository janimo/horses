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

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import *
from google.appengine.api import users
from google.appengine.api import mail
from google.appengine.api.labs import taskqueue

import ro

class MainHandler(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user == None:
            nick = "Not Signed in User"
        else:
            nick = user.nickname()
            nick = string.join(map(string.capitalize, string.split(nick)))

        template_values = {'username': nick, 'mail': ro.mail_body}
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))

class SendMail(webapp.RequestHandler):
    @login_required
    def get(self):
        user = users.get_current_user()
        user_address = user.email()
        user_name = self.request.str_GET["username"]

        if mail.is_email_valid(user_address):
            for mep in ro.meps:
                m, dest_address = mep.split()
                dest_address = 'jani.monoses+'+string.split(dest_address,'@')[0]+'@gmail.com'
                if m == "Mr":
                    greet = "Stimate Domnule Parlamentar"
                else:
                    greet = "Stimată Doamnă Parlamentar"

                mail.send_mail(user_address,
                        dest_address,
                        ro.mail_subj,
                        greet + ro.mail_body + user_name
                        )

        self.redirect('/done?meps=%d' % (len(ro.meps)))

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

