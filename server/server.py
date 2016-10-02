#!/usr/bin/python3

import cherrypy
import random
import string
import os, os.path
import sys
import Auth
import Main
import DB

from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('public/html'))

class Home(object):
    auth = Auth.AuthController()
    main = Main.MainController()

    @cherrypy.expose
    def index(self):
        try:
            if cherrypy.session[Auth.SESSION_KEY] is not None:
                raise cherrypy.HTTPRedirect("/main/matcher")
            else:
                raise KeyError
        except KeyError:
            tmpl = env.get_template('index.html')
            return tmpl.render(hero_image='hero_image.jpeg')

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
