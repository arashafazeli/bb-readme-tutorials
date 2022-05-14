from http.client import REQUEST_TIMEOUT
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS
from prometheus_client import Summary, make_wsgi_app, Counter
from werkzeug.middleware.dispatcher import DispatcherMiddleware

REQUEST_TIME = Summary("test_summary_request_time", "Time spent processing requests", ["endpoint"])
REQUEST_COUNTER = Counter("test_counter_requests", "Total requests", ["endpoint", "method"])

app = Flask(__name__)
CORS(app)

app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {"/metrics": make_wsgi_app()})

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
 
# Models
class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String)
    title = db.Column(db.String)
    text = db.Column(db.String)
    submitted = db.Column(db.TIMESTAMP)

    def as_dict(self):
        return {
            "id": self.id,
            "author": self.author,
            "title": self.title,
            "text": self.text,
            "submitted": self.submitted,
        }

    def __init__(self, author, title, text):
        self.author, self.title, self.text = author, title, text
        self.submitted = datetime.utcnow()

class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String)
    text = db.Column(db.String)
    submitted = db.Column(db.TIMESTAMP)

    parent = db.Column(db.Integer, db.ForeignKey('messages.id'),
        nullable=False)
    parent_rel = db.relationship('Message',
        backref=db.backref('comments', lazy=True))


    def as_dict(self):
        return {
            "id": self.id,
            "author": self.author,
            "text": self.text,
            "submitted": self.submitted,
            "parent" : self.parent
        }

    def __init__(self, author, text, parent):
        self.author, self.text, self.parent = author, text, parent
        self.submitted = datetime.utcnow()

@REQUEST_TIME.labels("/messages").time()
@app.route("/messages", methods=["GET", "POST"])
def messages(): 
    if request.method == "GET":
        REQUEST_COUNTER.labels("/messages", "get").inc()
        return {"data": [message.as_dict() for message in Message.query.all()]}
    elif request.method == "POST":
        REQUEST_COUNTER.labels("/messages", "post").inc()
        author = request.form['author']
        title = request.form['title']
        text = request.form['text']
        message = Message(author, title, text)
        db.session.add(message)
        db.session.commit()
        return{'data' : 'Message created'}


@REQUEST_TIME.labels("/comments").time()
@app.route("/comments", methods=["GET", "POST"])
def comments():
        if request.method == "GET":
            REQUEST_COUNTER.labels("/comments", "get").inc()
            return {"data": [comment.as_dict() for comment in Comment.query.all()]}
        elif request.method == "POST":
            REQUEST_COUNTER.labels("/comments", "post").inc()
            author = request.form['author']
            text = request.form['text']
            parent = request.form['parent']
            comment = Comment(author, text, parent)
            db.session.add(comment)
            db.session.commit()
            return{'data' : 'Comment created'}
    