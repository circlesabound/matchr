# Credit to original post from Amar Birgisson at 
# http://tools.cherrypy.org/wiki/AuthenticationAndAccessRestrictions

# Form based authentication for CherryPy. Requires the
# Session tool to be loaded.

import cherrypy
import urllib
import DB
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('public/html')) # Jinja2 environment

SESSION_KEY = '_cp_username'

def verify(username, password):
    """Verifies credentials for username and password.
    Returns user ID on success or a string describing the error on failure"""
    try:
        db = DB.DB("matchr.db")
        db.connect()
        userID = db.check_credentials(username, password)
        db.close()
        if userID:
            return userID
        else:
            raise ValueError("Incorrect username or password")
    except RuntimeError:
        return "Could not open database"

def check_auth(*args, **kwargs):
    """A tool that looks in config for 'auth.require'. If found and it
    is not None, a login is required and the entry is evaluated as alist of
    conditions that the user must fulfill"""
    conditions = cherrypy.request.config.get('auth.require', None)
    # format GET params
    get_parmas = urllib.parse.quote(cherrypy.request.request_line.split()[1])
    if conditions is not None:
        username = cherrypy.session.get(SESSION_KEY)
        if username:
            cherrypy.request.login = username
            for condition in conditions:
                # A condition is just a callable that returns true or false
                if not condition():
                    # Send old page as from_page parameter
                    raise cherrypy.HTTPRedirect("/auth/login?from_page=%s" % get_parmas)
        else:
            # Send old page as from_page parameter
            raise cherrypy.HTTPRedirect("/auth/login?from_page=%s" %get_parmas) 
    
cherrypy.tools.auth = cherrypy.Tool('before_handler', check_auth)

def require(*conditions):
    """A decorator that appends conditions to the auth.require config
    variable."""
    def decorate(f):
        if not hasattr(f, '_cp_config'):
            f._cp_config = dict()
        if 'auth.require' not in f._cp_config:
            f._cp_config['auth.require'] = []
        f._cp_config['auth.require'].extend(conditions)
        return f
    return decorate

# Conditions are callables that return True
# if the user fulfills the conditions they define, False otherwise
#
# They can access the current username as cherrypy.request.login
#
# Define those at will however suits the application.

def name_is(reqd_username):
    return lambda: reqd_username == cherrypy.request.login

# These might be handy

def any_of(*conditions):
    """Returns True if any of the conditions match"""
    def check():
        for c in conditions:
            if c():
                return True
        return False
    return check

# By default all conditions are required, but this might still be
# needed if you want to use it inside of an any_of(...) condition
def all_of(*conditions):
    """Returns True if all of the conditions match"""
    def check():
        for c in conditions:
            if not c():
                return False
        return True
    return check


# Controller to provide login and logout actions

class AuthController(object):
    
    def on_login(self, username):
        try:
            db = DB.DB("matchr.db")
            db.connect()
            userID = cherrypy.session[SESSION_KEY]
            cherrypy.session['user_details'] = db.get_user_details(userID)
        except ValueError:
            raise ValueError("Could not find user details")
        except RuntimeError:
            raise ValueError("Could not open database")
    
    def on_logout(self, username):
        """Called on logout"""
    
    def get_loginform(self, username, msg="Enter login information", from_page="/"):
        tmpl = env.get_template("login.html")
        return tmpl.render(user = username, message = msg, from_pg = from_page) 
        return """<html><body>
            <form method="post" action="/auth/login">
            <input type="hidden" name="from_page" value="%(from_page)s" />
            %(msg)s<br />
            Username: <input type="text" name="username" value="%(username)s" /><br />
            Password: <input type="password" name="password" /><br />
            <input type="submit" value="Log in" />
        </body></html>""" % locals()
    
    @cherrypy.expose
    def login(self, username=None, password=None, from_page="/"):
        if username is None or password is None:
            return self.get_loginform("", from_page=from_page)
        
        try:
            userID = verify(username, password)
            cherrypy.session[SESSION_KEY] = cherrypy.request.login = userID
            self.on_login(userID)
            raise cherrypy.HTTPRedirect(from_page or "/")
        except ValueError as e:
            return self.get_loginform(username, e.args, from_page)
    
    @cherrypy.expose
    def logout(self, from_page="/"):
        sess = cherrypy.session
        username = sess.get(SESSION_KEY, None)
        sess[SESSION_KEY] = None
        if username:
            cherrypy.request.login = None
            self.on_logout(username)
        raise cherrypy.HTTPRedirect(from_page or "/")