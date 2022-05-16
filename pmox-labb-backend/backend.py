from http.client import REQUEST_TIMEOUT
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS
from prometheus_client import Summary, make_wsgi_app, Counter
from werkzeug.middleware.dispatcher import DispatcherMiddleware

# ==================== Variabels for prometheus_client ====================
REQUEST_TIME = Summary("test_summary_request_time", "Time spent processing requests", ["endpoint"])
REQUEST_COUNTER = Counter("test_counter_requests", "Total requests", ["endpoint", "method"])

app = Flask(__name__)
# ==================== Cross Origin Resource Sharing (CORS), making cross-origin AJAX possible ====================
CORS(app)


# ==================== Endpoint to Prometheus ====================
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {"/metrics": make_wsgi_app()})


# ==================== Variables for SQLAlchemy and PostgreSQL ====================
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
 

# ==================== Variables for table 'messages' in database ====================
class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String)
    title = db.Column(db.String)
    text = db.Column(db.String)
    submitted = db.Column(db.TIMESTAMP)


# ==================== self.submitted i a datestamp Coordinated Universal Time  ====================
    def as_dict(self):
        return {
        "id": self.id,
        "author": self.author,
        "title":self.title,
        "text": self.text,
        "submitted": self.submitted,
            
        }
    
    
    def __init__(self, author, title, text):
        self.author, self.title, self.text = author, title, text
        self.submitted = datetime.utcnow()


# ==================== Variables for table 'comments' in database ====================
class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String)
    text = db.Column(db.String)
    submitted = db.Column(db.TIMESTAMP)


# ==================== parent is the message the comment refers to ====================
    parent = db.Column(db.Integer, db.ForeignKey('messages.id'),
        nullable=False)
    parent_rel = db.relationship('Message',
        backref=db.backref('comments', lazy=True))


# ================== Function is used in for-loops at row 80 and 97 ===================================
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


# ==================== GET or POST requests /messages ====================
@REQUEST_TIME.labels("/messages").time() # Counter to prometheus_client
@app.route("/messages", methods=["GET", "POST"])
def messages(): 
    if request.method == "GET":
        REQUEST_COUNTER.labels("/messages", "get").inc() # Counter to prometheus_client
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

# ==================== GET or POST requests /comments ====================
@REQUEST_TIME.labels("/comments").time() # Counter to prometheus_client
@app.route("/comments", methods=["GET", "POST"])
def comments():
        if request.method == "GET":
            REQUEST_COUNTER.labels("/comments", "get").inc() # Counter to prometheus_client
            return {"data": [comment.as_dict() for comment in Comment.query.all()]}
        elif request.method == "POST":
            REQUEST_COUNTER.labels("/comments", "post").inc() # Counter to prometheus_client
            author = request.form['author']
            text = request.form['text']
            parent = request.form['parent']
            comment = Comment(author, text, parent)
            db.session.add(comment)
            db.session.commit()
            return{'data' : 'Comment created'}
    