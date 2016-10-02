import cherrypy
import DB
import Auth
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('public/html')) # Jinja2 environment

class MainController(object):
    @cherrypy.expose
    @Auth.require()
    def matcher(self):
        tmpl = env.get_template('matcher.html')
        # encodedImage = cherrypy.session['user_details']['image']
        # return tmpl.render(image=encodedImage)
        return tmpl.render()

    @cherrypy.expose
    def signup(self):
        tmpl = env.get_template('signup.html')
        return tmpl.render()

    def register(self):
        pass