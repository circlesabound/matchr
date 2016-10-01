#!/usr/bin/python3

import cherrypy
import random
import string
import os, os.path
import Auth
import sys

from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('public/html'))

class Home(object):
    auth = Auth.AuthController()

    @cherrypy.expose
    def index(self):
        tmpl = env.get_template('index.html')
        return tmpl.render(name='John')

    @cherrypy.expose
    def generate(self, length=8):
        some_string = ''.join(random.sample(string.hexdigits, int(length)))
        cherrypy.session['mystring'] = some_string
        tmpl = env.get_template('generator.html')
        return tmpl.render(string=some_string)

    @cherrypy.expose
    @Auth.require(Auth.name_is("joe"))
    def only_for_joe(self):
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

    if len(sys.argv) > 1 and sys.argv[1] == "--web":
        cherrypy.server.socket_port = 80
        cherrypy.server.socket_host = '0.0.0.0'
    cherrypy.quickstart(Home(), '/', conf)
