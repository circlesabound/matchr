import cherrypy
import DB
import Auth
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('public/html')) # Jinja2 environment

class MainController(object):
    @cherrypy.expose
    @Auth.require()
    def matcher(self):
        db = DB.DB('matchr.db')
        db.connect()
        match_id = db.get_next_match(cherrypy.session['user_details']['user_id'])
        if match_id is None:
            return env.get_template('dead_matcher.html').render()
        tmpl = env.get_template('matcher.html')
        gender = ""
        if match_details["gender"] is not None:
            gender = match_details["gender"].upper()
        return tmpl.render(
            first_name=match_details['first_name'],
            last_name=match_details['last_name'],
            age="",
            gender=gender,
            image=match_details['image'],
            description=match_details['description'])

    @cherrypy.expose
    @Auth.require()
    def reject(self):
        pass
