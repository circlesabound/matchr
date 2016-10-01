#!/usr/bin/python3

import cherrypy

class Matchr(object):
	@cherrypy.expose
	def index(self):
		return "hello there"

if __name__ == '__main__':
	cherrypy.server.socket_port = 80
	cherrypy.server.socket_host = '0.0.0.0'
	cherrypy.quickstart(Matchr())

