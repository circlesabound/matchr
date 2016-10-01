#!/usr/bin/python3

import cherrypy
import random
import string
import os, os.path
import Auth

class Home(object):
    auth = Auth.AuthController()

    @cherrypy.expose
    def index(self):
        return """<html>
          <head>
            <link href="/static/css/style.css" rel="stylesheet">
          </head>
          <body>
            <form method="get" action="only_for_joe">
              <input type="text" value="8" name="length" />
              <button type="submit">Give it now!</button>
            </form>
          </body>
        </html>"""

    @cherrypy.expose
    def open(self, length=8):
        return """This page is open to everyone"""

    @cherrypy.expose
    @Auth.require(Auth.name_is("joe"))
    def only_for_joe(self, length):
        return """Hello Joe - this page is available to you only"""


if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd()),
            'tools.auth.on': True
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }


    cherrypy.quickstart(Home(), '/', conf)