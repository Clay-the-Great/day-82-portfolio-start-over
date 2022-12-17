import requests
from flask import Flask, render_template, redirect, url_for, flash, request, abort
from flask_bootstrap import Bootstrap
# from flask_ckeditor import CKEditor
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
# from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
# from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm, DeletionForm
from flask_gravatar import Gravatar
from functools import wraps
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import os

BOT_TOKEN = "5741115248:AAFgEELGcwLMkUwfhQiiX82POBauG1cLpBk"
BOT_CHATID = "5016448629"
# BOT_TOKEN = os.environ.get("BOT_TOKEN")
# BOT_CHATID = os.environ.get("BOT_CHATID")

app = Flask(__name__)
# app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
# ckeditor = CKEditor(app)
Bootstrap(app)

# CONNECT TO DB
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///blog.db")
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL_ALT", "sqlite:///blog.db")
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

# gravatar = Gravatar(app,
#                     size=100,
#                     rating='g',
#                     default='retro',
#                     force_default=False,
#                     force_lower=False,
#                     use_ssl=False,
#                     base_url=None)

owners = [1]
# login_manager = LoginManager()
# login_manager.init_app(app)


# CONFIGURE TABLES
# class User(db.Model, UserMixin):
#     __tablename__ = "user"
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(250), unique=True, nullable=False)
#     password = db.Column(db.String(250), nullable=False)
#     name = db.Column(db.String(250), nullable=False)
#     posts = relationship("BlogPost", back_populates="author")
#     comments = relationship("Comment", back_populates="author")


# class BlogPost(db.Model):
#     __tablename__ = "blog_posts"
#     id = db.Column(db.Integer, primary_key=True)
#     # author = db.Column(db.String(250), nullable=False)
#     title = db.Column(db.String(250), unique=True, nullable=False)
#     subtitle = db.Column(db.String(250), nullable=False)
#     date = db.Column(db.String(250), nullable=False)
#     body = db.Column(db.Text, nullable=False)
#     img_url = db.Column(db.String(250), nullable=False)
#     author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     author = relationship("User", back_populates="posts")
#     comments = relationship("Comment", back_populates="parent_blog")
#
#
# class Comment(db.Model):
#     __tablename__ = "comments"
#     id = db.Column(db.Integer, primary_key=True)
#     text = db.Column(db.Text, nullable=False)
#     time = db.Column(db.String(250), nullable=False)
#     author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     author = relationship("User", back_populates="comments")
#     blog_id = db.Column(db.Integer, db.ForeignKey('blog_posts.id'))
#     parent_blog = relationship("BlogPost", back_populates="comments")


# db.create_all()
logged_in = False
current_user_id = 0


# def admin_only(function):
#     @wraps(function)
#     def wrapper_function(*args, **kwargs):
#         if current_user_id == 1:
#             return function(*args, **kwargs)
#         else:
#             return abort(403, "You are not authorized to view this page, sucker hahaha.")
#     return wrapper_function


@app.route('/')
def get_all_posts():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html", logged_in=logged_in)


@app.route("/contact", methods=["POST", "GET"])
def contact():
    is_successful = False
    if request.method == "GET":
        return render_template("contact.html", logged_in=logged_in, is_successful=is_successful)
    elif request.method == "POST":
        name = request.form["username"]
        email = request.form["email"]
        phone = request.form["phone"]
        message = request.form["message"]

        bot_message = f"Personal Website Viewer Message\n\n" \
                      f"Name: {name}\n" \
                      f"Email: {email}\n" \
                      f"Phone: {phone}\n" \
                      f"Message: {message}"

        send_telegram_message = 'https://api.telegram.org/bot' + BOT_TOKEN + '/sendMessage?chat_id=' + \
                                BOT_CHATID + '&parse_mode=Markdown&text=' + bot_message
        requests.get(send_telegram_message)

        is_successful = True
        return render_template("contact.html", logged_in=logged_in, is_successful=is_successful)


@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}


if __name__ == "__main__":
    app.run(debug=True)
