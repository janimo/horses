#!/usr/bin/env python
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

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp.util import login_required
from google.appengine.api import users
from google.appengine.api import mail


class MainHandler(webapp.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if user == None:
	nick = "alma ata"
    else:
        nick = user.nickname()
    nick = string.join(map(string.capitalize, string.split(nick)))
    self.response.out.write("Hello %s ! <a href='/mail'>Send</a> mail!"	% (nick))

class SendMail(webapp.RequestHandler):
  @login_required
  def get(self):
    user_address = users.get_current_user().email()
    if mail.is_email_valid(user_address):
	    mail.send_mail(user_address, user_address, "Test GAE", """
	    Hello from GAE!
	    """)
    self.response.out.write("Sent to email: " + user_address)


def main():
  application = webapp.WSGIApplication([
	  				('/', MainHandler),
	  				('/mail', SendMail),
					],
                                       debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
  main()
