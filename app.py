from flask import Flask,render_template,request,session,redirect
import os
import pathlib
import shutil
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail,Message
from datetime import datetime
import json


with open("templates/config.json","r") as c:
    params = json.load(c)["params"]

localServer = True
app = Flask(__name__)
app.secret_key = "sskey"
app.config.update(
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_PORT = "465",
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params["mailUser"],
    MAIL_PASSWORD = params["mailPassword"]
)
app.config['UPLOAD_FOLDER'] = params['uploadLocation']

mail = Mail(app)

if(localServer):
    app.config["SQLALCHEMY_DATABASE_URI"] = params["localUrl"]
    app.config["SQLALCHEMY_BINDS"] = {
    "blog":params["blogUrl"],
    "news":params["newsletter"],
    "users":params["userdb"]
}
    
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = params["prodUrl"]



# from project import app, db
# >>> app.app_context().push()
# >>> db.create_all()

app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
db = SQLAlchemy(app)

class Contact(db.Model):
    sno = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(50),nullable = False)
    phoneNo = db.Column(db.String(50),nullable = False)
    email = db.Column(db.String(50),nullable = False)
    desc = db.Column(db.String(500),nullable = False)
    date = db.Column(db.DateTime, default = datetime.now().strftime("%c")[0:11])

    def __repr__(self) -> str:
        return f"{self.sno} - {self.name}"


class Blog(db.Model):
    __bind_key__ = "blog"
    sno = db.Column(db.Integer,primary_key = True)
    slug = db.Column(db.String(25),nullable = False)
    title = db.Column(db.String(50),nullable = False)
    subtitle = db.Column(db.String(50),nullable = False)
    content = db.Column(db.String(500),nullable = False)
    author = db.Column(db.String(50),nullable = False)
    date = db.Column(db.String(11), default = datetime.now().strftime("%c")[0:11])

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

class Newsletter(db.Model):
    __bind_key__ = "news"
    sno = db.Column(db.Integer,primary_key = True)
    email = db.Column(db.String(25),nullable = False)
    date = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.name}"


class Users(db.Model):
    __bind_key__ = "users"
    sno = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(25),nullable = False)
    email = db.Column(db.String(50),nullable = False)
    password = db.Column(db.String(50),nullable = False)
    fpass = db.Column(db.String(50),nullable = False)
    date = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.name}"
    



@app.route("/signin",methods=["GET","POST"])
def signin():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        fpass = request.form["fpass"]
        if(password==fpass):
             user = Users(name =name,email = email,password=password,fpass=fpass )
             db.session.add(user)
             db.session.commit()
             return "<body><script>alert('You Joined')</script></body>"
        else:
             return "<body><script>alert('Password done not match')</script></body>"
             
        

       
    user = Users.query.all()
   
    return render_template("signin.html",user = user,params=params)
    



@app.route("/")
def landingPage():
    blog = Blog.query.all()
    return render_template("index.html",params=params,blog = blog)

@app.route("/about")
def about():
    return render_template("about.html",params=params)

@app.route("/data")
def data():
    return render_template("data.html",params=params)

@app.route("/contact",methods = ["GET","POST"])
def contact():
     if request.method == "POST":
        name = request.form["name"]
        phoneNo = request.form["phoneNo"]
        email = request.form["email"]
        desc = request.form["desc"]
        entry = Contact(name =name,email = email, phoneNo = phoneNo,desc = desc)
        db.session.add(entry)
        db.session.commit()
       
     entry = Contact.query.all()
     return render_template("contact.html",entry = entry,params=params)




@app.route("/blog/<string:slug>",methods = ['GET'])
def blog(slug):
    try:
        blog = Blog.query.filter_by(slug = slug).first()
        return render_template("blog.html",blog = blog,params=params)
    except:
        return "<body><script>alert('This is our last Article')</script></body>"


    

@app.route("/explore")
def explore():
    blog = Blog.query.all()
    return render_template("explore.html",blog = blog,params=params)
    

@app.route("/dashboard",methods =["GET","POST"])
def dashboard():
    if("user" in session and session["user"]==params["admin"]):
        blog = Blog.query.all()
        entry = Contact.query.all()
        return render_template("dashboard.html",params=params,blog = blog,entry = entry)
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        if(username == params["admin"] and password == params["adminPassword"]):
            session["user"]= username
            blog = Blog.query.all()
            entry = Contact.query.all()
            return render_template("dashboard.html",params = params, blog = blog,entry = entry )

    
    return render_template("adminLogin.html",
    params=params)




@app.route("/blogAdmin",methods=["GET","POST"])
def blogAdmin():
     if("user" in session and session["user"]==params["admin"]):
         if request.method == "POST":
            slug = request.form["slug"]
            title = request.form["title"]
            subtitle = request.form["subtitle"]
            f = request.files['file1']
            author = request.form["author"]
            content = request.form["content"]
            filename = secure_filename(f.filename)
            ext = pathlib.Path(filename).suffix  # get file extension
            new_filename = slug + ext
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            shutil.move(os.path.join(app.config['UPLOAD_FOLDER'], filename), os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
            blog = Blog(slug = slug,title =title,subtitle = subtitle, author = author,content = content)
            db.session.add(blog)
            db.session.commit()
            return redirect("/dashboard")
         
         blog = Blog.query.all()
         return render_template("blogAdmin.html",blog = blog,params=params)




@app.route("/update/<string:slug>",methods = ["GET","POST"])
def update(slug):
     if("user" in session and session["user"]==params["admin"]):
        if request.method == "POST":
            slug = request.form["slug"]
            title = request.form["title"]
            subtitle = request.form["subtitle"]
            f = request.files['file1']
            content = request.form["content"] 
            filename = secure_filename(f.filename)
            ext = pathlib.Path(filename).suffix  # get file extension
            new_filename = slug + ext
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            shutil.move(os.path.join(app.config['UPLOAD_FOLDER'], filename), os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
            author = request.form["author"]
            blog = Blog.query.filter_by(slug = slug).first()
            blog.slug = slug
            blog.title = title
            blog.subtitle = subtitle
            blog.content = content
            blog.author = author
            db.session.add(blog)
            db.session.commit()
            return redirect("/dashboard")
        
    
        blog = Blog.query.filter_by(slug = slug).first()
        return render_template("update.html",blog = blog,params=params)


@app.route("/delate/<string:slug>")
def delate(slug):
     if("user" in session and session["user"]==params["admin"]):
        if os.path.exists(params["uploadLocation"]+f"\\{slug}.jpg"):
            os.remove(params["uploadLocation"]+f"\\{slug}.jpg")
        blog = Blog.query.filter_by(slug = slug).first()
        db.session.delete(blog)
        db.session.commit()
        return redirect("/dashboard")


@app.route("/logout")
def logout():
     if("user" in session and session["user"]==params["admin"]):
        session.pop("user")
        return redirect("/dashboard")