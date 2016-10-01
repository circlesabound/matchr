#!/usr/bin/python3

import cherrypy
import random
import string
import os, os.path

from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('public/html'))

class Matchr(object):
    @cherrypy.expose
    def index(self):
        #f = open ('public/html/index.html', 'r') # open does not take cherrypy url
        #return f.read()
        tmpl = env.get_template('index.html')
        return tmpl.render(name='John')

    @cherrypy.expose
    def generate(self, length=8):
        some_string = ''.join(random.sample(string.hexdigits, int(length)))
        cherrypy.session['mystring'] = some_string
        tmpl = env.get_template('generator.html')
        return tmpl.render(string=some_string)

    @cherrypy.expose
    def display(self):
        return cherrypy.session['mystring']

if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }
    cherrypy.quickstart(Matchr(), '/', conf)
