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
    def signup(self, username="", password="", age="", description="",
               gender="", code_sample=None, profile_img=None):
        try:
            if username == "" or password == "":
                return self.get_registration_form("", "Please enter your email or password");
            if age == "":
                return self.get_registration_form(username, "Please enter your age")
            if int(age) < 18:
                return self.get_registration_form(username, "Please enter a valid age")
            if gender is None:
                return self.get_registration_form(username, "Please select your gender")
            if code_sample == "":
                return self.get_registration_form(username, "Please upload a sample of your code")
        except ValueError as e:
            return self.get_registration_form(username, "Please enter a valid age")
        
        if description is None:
            description = ""

        codeFile = self.upload(code_sample)
        # imgFile = self.upload(profile_img)

        return codeFile

    def get_registration_form(self, username, msg="Join us by making an account"):
        tmpl = env.get_template("signup.html")
        return tmpl.render(user = username, message = msg)

    def get_success_msg(self, username):
        tmpl = env.get_template("signup_success.html")
        return tmpl.render(user = username)

    def upload(self, f):
        while True:
            data = f.file.read(8192)
            if not data:
                break

        return data