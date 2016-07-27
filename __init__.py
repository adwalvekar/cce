from flask import Flask, render_template, url_for, abort, request
from flask_sqlalchemy import SQLAlchemy 

#App Definition
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
app.debug= True
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Bangalore12E@localhost/cce'

class Post(db.Model):
	pid = db.Column(db.Integer , primary_key = True)
	slug = db.Column(db.String(100))
	title = db.Column(db.String(300))
	content = db.Column(db.Text(5000), unique=False)
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

class emails(db.Model):
	eid = db.Column(db.SmallInteger,primary_key = True)
	email = db.Column(db.String(100))
	def __init__(self, email):
		self.email = email
#Routes
def slugify(title):
	s= title
	s.replace(" ", "-")
	s.replace("/", "-")
	s.lower()
	return s
@app.route('/')
def index():
	return "Hello World"
@app.route('/posts')
def post():
	return "All Posts"
@app.route('/post/<string:slug>')
def specific_post(slug):
	print slugify(slug)
	return slugify(slug)
@app.route('/make/admin',methods=['GET', 'POST'])
def make_admin():
	if request.method == 'GET':
		return render_template('make.html', success= '')
	else:
		if request.form['upass'] == 'Bangalore12E':
			user = User(request.form['username'], request.form['password'], True)
			db.session.add(user)
			db.session.commit()
			return render_template('make.html', success = 'success')
		else:
			abort(401)
@app.route('/make/post', methods= ['POST','GET'])
def make_post():
	if method == 'POST':
		pass
	else :
		return render_template('post.html')
	pass
#Create DB
db.create_all()
#Run
if __name__=='__main__':
	app.run()