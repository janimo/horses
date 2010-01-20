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

import ro

class MainHandler(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user == None:
            nick = ""
        else:
            nick = user.nickname()
            nick = string.join(map(string.capitalize, string.split(nick)))

        template_values = {'username': nick}
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))

class SendMail(webapp.RequestHandler):
    @login_required
    def get(self):
        user = users.get_current_user()
        user_address = user.email()
        user_name = self.request.str_GET["username"]

        i = 0
        if mail.is_email_valid(user_address):
            for mep in ro.meps:
                i += 1
                m, dest_address = mep.split()
                if m == "Mr":
                    greet = "Stimate Domnule Parlamentar"
                else:
                    greet = "Stimată Doamnă Parlamentar"

                mail.send_mail(user_address,
                               dest_address,
                               ro.mail_subj,
                               greet + ro.mail_body
                               + user_name,
                               )

        self.response.out.write("Emails sent to %d MEPs. Check your GMail Sent folder for proof." % (i))

def main():
    application = webapp.WSGIApplication([
        ('/', MainHandler),
        ('/mail', SendMail),
        ],
        debug=True)
    run_wsgi_app(application)


if __name__ == '__main__':
    main()

# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab

