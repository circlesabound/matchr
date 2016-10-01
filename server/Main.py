import cherrypy
import DB
import Auth
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('public/html')) # Jinja2 environment

class MainController(object):
    @cherrypy.expose
    @Auth.require()
    def find_matches(self):
        tmpl = env.get_template('find_matches.html')
        encodedImage = cherrypy.session['user_details']['image']
        return tmpl.render(image=encodedImage)