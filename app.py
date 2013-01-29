import web
import polynomial
from pymongo import Connection
from mongodb import users
import json


render = web.template.render('templates/')

urls = (
            '/', 'index',
            '/demo', 'demo',
            '/howitworks', 'howitworks',
            '/signup', 'signup',
            '/login', 'login',
            '/logout', 'logout',
            '/latexquery', 'latexquery',
            '/practice', 'practice'
            )

app = web.application(urls, globals())


#First get a MongoDB database object
c = Connection()
db = c.webpy


def setup():
    users.collection = db.users
    users.SALTY_GOODNESS = u'RANDOM_SALT'

    app.run()


def set_user_loggedin_cookie(user):
    cookieString = user['name'] + "%" + user['email']
    web.setcookie('loggedin', cookieString, 3600*24)


def get_user_loggedin():
    cookie = web.cookies().get("loggedin")
    if cookie and cookie != "NULL":
        cookieTokens = cookie.split("%")
        return (True, cookieTokens[0])
    else:
        return (False, "")


def nullify_user_cookie():
    cookie = web.cookies().get("loggedin")
    if cookie:
        web.setcookie('loggedin', "NULL", 3600)


class login:
    def GET(self):
        #go to where a logged-in user would go (/)
        #else:
        #    Go to the auxiliary login page (the dropdown login attempt failed)
        data = web.input(failed="false", email="")
        isLoggedin, username = get_user_loggedin()
        if isLoggedin:
            web.seeother('/')
        else:
            loginFailed = False
            msg = data.email
            if data.failed == "true":
                loginFailed = True
            return render.login(loginFailed, msg)

    def POST(self):
        email, password = (web.input().email, web.input().password)

        user = users.authenticate(email, password)
        if user:
            set_user_loggedin_cookie(user)
            print "Logged in"
            web.seeother('/')
        else:
            #Handle your login failure
            print "Error in logging in"
            web.seeother('login?failed=true&email=' + email)


class logout:
    def GET(self):
        nullify_user_cookie()
        web.seeother('/')


class index:
    def GET(self):
        isLoggedin, username = get_user_loggedin()
        return render.index(isLoggedin, username)


class demo:
    def GET(self):
        return render.demo()


class howitworks:
    def GET(self):
        isLoggedin, username = get_user_loggedin()
        return render.howitworks(isLoggedin, username)


class signup:
    def GET(self):
        isLoggedin, username = get_user_loggedin()
        if isLoggedin:
            web.seeother('/')
        return render.signup()

    def POST(self):
        name, email, password = (web.input().name,
                                                   web.input().email,
                                                   web.input().password)
        user = users.register(name=name,
                                    password=users.pswd(password),
                                    email=email)

        #Returns None if the user already exists
        if not user:
            print "User already exists"

        set_user_loggedin_cookie(user)
        web.seeother('/')

        print "POST: " + "\nname= " + name + "\nemail= " + email + "\npassword= " + password


class latexquery:
    def GET(self):
        isLoggedin, username = get_user_loggedin()
        if isLoggedin:
            data = web.input(q="none")
            if data.q == "algebra":
                factorised_question = polynomial.gen_random_factorised_polynomial_equal_zero(3, -2, 3)
                sym_question = factorised_question.expand()
                latex_question = polynomial.latex_polynomial(sym_question)
                answer = (polynomial.latex_polynomial(
                    factorised_question) + 
                    polynomial.latex_solutions(polynomial.solve(sym_question)))
                return json.dumps({"question":latex_question, "answer":answer}, sort_keys=False)
        else:
            web.seeother('/login')


class practice:
    def GET(self):
        isLoggedin, username = get_user_loggedin()
        if isLoggedin:
            return render.practice(isLoggedin,username)
        else:
            web.seeother('/login')


if __name__ == "__main__":
    setup()
