#!/usr/bin/python3

import cherrypy

class Matchr(object):
	@cherrypy.expose
	def index(self):
		return "hello there"

if __name__ == '__main__':
	cherrypy.quickstart(Matchr())

