from flask import Flask, render_template, url_for, abort, request
from flask_sqlalchemy import SQLAlchemy 
import json
import urllib2
import pprint
from flask_mail import Mail, Message
#App Definition
with open('./config.json') as c:
	config = json.load(c)
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
app.config['MAIL_SERVER'] = config['mail_server']
app.config['MAIL_PORT'] = config['port']
app.config['MAIL_USE_SSL'] = config['SSL']
app.config['MAIL_USERNAME'] = config['username']
app.config['MAIL_PASSWORD'] = config['password']
db = SQLAlchemy(app)
mail = Mail(app)
app.config['SQLALCHEMY_DATABASE_URI'] = config['db_uri']
SITE_KEY = config['captcha_site_key']
SECRET_KEY= config['captcha_secret_key']
def slugify(title):
	s= title
	s.replace(" ", "-")
	s.replace("/", "-")
	s.lower()
	return s
def checkRecaptcha(response, secretkey):
    url = 'https://www.google.com/recaptcha/api/siteverify?'
    url = url + 'secret=' +secretkey
    url = url + '&response=' +response
    try:
        jsonobj = json.loads(urllib2.urlopen(url).read())
        if jsonobj['success']:
            return True
        else:
            return False
    except Exception as e:
        return False
#Models
class Post(db.Model):
	pid = db.Column(db.Integer , primary_key = True)
	slug = db.Column(db.String(100), unique = True)
	title = db.Column(db.String(300))
	content = db.Column(db.Text, unique=False)
	file = db.Column(db.String(400),unique=False)
	create_date= db.Column(db.DateTime(timezone='IST'), unique=False)

	def __init__(self, title, content, file, create_date):
		self.title = title
		self.slug = slugify(title)
		self.content = content
		self.file = file
		self.create_date = create_date
		
	def __repr__():
		pass
class User(db.Model):
	uid = db.Column(db.SmallInteger, primary_key = True)
	username = db.Column(db.String(20))
	password = db.Column(db.String(40))
	admin = db.Column(db.Boolean())
	def __init__(self, username, password, admin):
		self.username = username
		self.password = password
		self.admin = admin

class Email(db.Model):
	eid = db.Column(db.SmallInteger,primary_key = True)
	email = db.Column(db.String(100))
	def __init__(self, email):
		self.email = email
		def __repr__():
			return self.email
#Routes
@app.route('/')
def index():
	return "Hello world!"
@app.route('/posts')
def post():
	return "All Posts"
@app.route('/post/<string:slug>')
def specific_post(slug):
	return slugify(slug)
@app.route('/make/admin',methods=['GET', 'POST'])
def make_admin():
	if request.method == 'GET':
		return render_template('make.html', success= '')
	else:
		if request.form['upass'] == config['admin_password']:
			user = User(request.form['username'], request.form['password'], True)
			db.session.add(user)
			db.session.commit()
			return render_template('make.html', success = 'success')
		else:
			abort(401)
@app.route('/add/post', methods= ['POST','GET'])
def make_post():
	if request.method == 'POST':
		pass
	else :
		return render_template('post.html')
	pass
@app.route('/add/email', methods=['POST', 'GET'])
def add_mail():
	if request.method == "POST":
		response = request.form.get('g-recaptcha-response')
		if checkRecaptcha(response,SECRET_KEY):
			db.session.add(email)
			db.session.commit()
			return render_template('addemail.html',success = True)
		else:
			return render_template('addemail.html', fail = True)
	else:
		return render_template('addemail.html', normal = True)
@app.route('/view/email')
def viewemail():
	ab = []
	a = Email.query.all()
	for x in a:
		ab.append(x.email)
	return str(ab)
#Create DB
db.create_all()
#Run
if __name__=='__main__':
	app.run(debug = True)