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
        user_details = cherrypy.session['user_details']
        gender = ""
        if user_details["gender"] is not None:
        	gender = user_details["gender"].upper()
        return tmpl.render(
        	first_name=user_details['first_name'],
        	last_name=user_details['last_name'],
        	age="",
        	gender=gender,
        	image=user_details['image'],
        	description=user_details['description']
        )
