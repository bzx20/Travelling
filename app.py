# Backend app for the Admin system
# Based on Flask

from flask import Flask, request, render_template, redirect, url_for, session, flash
from flasgger import swag_from, Swagger
# from models.model import Admin, Notice, Activity, Ticket
from login_required import login_required
from flask_sqlalchemy import SQLAlchemy
# import datetime
# from extensions import db

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:2Cwzack^gvcLaB@101.42.136.45:3306/cili?ssl_key=client-key.pem&ssl_cert=client-cert.pem&ssl_ca=ca-cert.pem'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:2Cwzack^gvcLaB@101.42.136.45:3306/cili'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config.from_object('config')
app.config['MySQL_HOST'] = '101.42.136.45'
app.config['MySQL_USER'] = 'root'
app.config['MySQL_PASSWORD'] = '2Cwzack^gvcLaB'
app.config['MySQL_DB'] = 'cili'
app.config['MySQL_PORT'] = 3306

db=SQLAlchemy(app)

# Create the database model
class Admin(db.Model):
    # Admin of the system
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True,doc='Admin ID')
    adminname = db.Column(db.String(20), unique=True, nullable=False,doc='Admin name')
    password = db.Column(db.String(20), nullable=False,doc='Admin password')
    authority = db.Column(db.Integer, nullable=False,doc='Admin authority')

    def __repr__(self):
        return f"Admin('{self.adminname}', '{self.password}')"



class Announcement(db.Model):
    # Announcement of the system
    __tablename__ = 'announcement'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True,doc='Announcement ID')
    title = db.Column(db.String(100), nullable=False,doc='Announcement title')
    content = db.Column(db.Text, nullable=False,doc='Announcement content')
    date = db.Column(db.DateTime, nullable=False,doc='Announcement date')
    is_publish = db.Column(db.Boolean, nullable=False,doc='Announcement is to publish')

    def __repr__(self):
        return f"Announcement('{self.title}', '{self.content}')"

class Activity(db.Model):
    # Activity of the system
    __tablename__ = 'activity'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True,doc='Activity ID')
    title = db.Column(db.String(100), nullable=False,doc='Activity title')
    content = db.Column(db.Text, nullable=False,doc='Activity content')
    specy = db.Column(db.String(20), nullable=False,doc='Activity specy')
    begin_date = db.Column(db.Date, nullable=False,doc='Activity start date')
    end_date = db.Column(db.Date, nullable=False,doc='Activity end date')
    num = db.Column(db.Integer, nullable=False,doc='Activity number')

    def __repr__(self):
        return f"Activity('{self.title}', '{self.content}')"

class Ticket(db.Model):
    # Ticket of the system
    __tablename__ = 'ticket'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True,doc='Ticket ID')
    key = db.Column(db.String(20), unique=True, nullable=False,doc='Ticket key')
    label = db.Column(db.Integer, nullable=False,doc='Ticket label')
    level = db.Column(db.Integer, nullable=False,doc='Ticket level')

    def __repr__(self):
        return f"Ticket('{self.key}', '{self.label}')"

class Comment(db.Model):
    # Comment of the systme
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True,doc='Comment ID')
    author = db.Column(db.Integer, nullable=False,doc='Comment author')
    content = db.Column(db.Text, nullable=False,doc='Comment content')
    date = db.Column(db.Date, nullable=False,doc='Comment date')
    time = db.Column(db.Time, nullable=False,doc='Comment time')
    is_forbidden = db.Column(db.Boolean, nullable=False,doc='Comment is forbidden')

    def __repr__(self):
        return f"Comment('{self.author}', '{self.content}')"

class Author(db.Model):
    # Author of the system
    __tablename__ = 'author'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True,doc='Author ID')
    name = db.Column(db.String(20), nullable=False,doc='Author name')
    # comments = db.relationship('Comment', backref='author', lazy=True,doc='Author comments')
    is_forbidden = db.Column(db.Boolean, nullable=False,doc='Author is forbidden')

    def __repr__(self):
        return f"Author('{self.name}')"

with app.app_context():
    db.drop_all()
    db.create_all()
Swagger(app)

# Create the routes
@app.route('/')
def index():
    return {'message': 'Hello, World!'}, 200

@swag_from('swagger/login.yml')
@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        data = request.get_json()
        if request.method == 'POST':
            # Check if the input adminname and password is in the database
            adminname = data['adminname']
            password = data['password']
            admin = Admin.query.filter_by(adminname=adminname).first()
            if admin:
                if password == admin.password:
                    return {'message': 'OK','authority': admin.authority}, 200
                else:
                    return {'message': 'Wrong password!'}, 404
            else:
                return {'message': 'Admin not found!'}, 404
    except:
        return {'message': 'Failed!'}, 404



# @login_required
@swag_from('swagger/logout.yml')
@app.route('/logout', methods=['POST'])
def logout():
    data = request.get_json()
    try:
        id = data['id']
        session.pop(id, None)
        return {'message': 'OK'}, 200
    except:
        return {'message': 'Failed!'}, 404

# @login_required
@app.route('/api/authority', methods=['POST'])
# Get the authority of the admin
def get_authority():
    data = request.get_json()
    try:
        id = data['id']
        admin = Admin.query.filter_by(id=id).first()
        return {'message': 'OK','authority': admin.authority}, 200
    except:
        return {'message': 'Not authorized!'}, 404



# @login_required
@swag_from('swagger/announcement.yml')
@app.route('/api/announcement/delete', methods=['POST'])
# Delete an announcement
def delete_annoucement():
    data = request.get_json()
    id = data['id']
    try:
        announcement = Announcement.query.filter_by(id=id).first()
        db.session.delete(announcement)
        db.session.commit()
        return {'message': 'OK'}, 200
    except:
        return {'message': 'Not Found'}, 404

# @swag_from('swagger/announcement.yml')
@login_required
@app.route('/api/announcement/get', methods=['POST'])
# Get the content of an announcement
def get_annoucement():
    data = request.get_json()
    id = data['id']
    try:
        announcement = Announcement.query.filter_by(id=id).first()
        return {'message': 'OK','id':announcement.id,'title': announcement.title,'content': announcement.content,'date': announcement.date}, 200
    except:
        return {'message': 'Not Found'}, 404

# @swag_from('swagger/announcement.yml')
@login_required
@app.route('/api/announcement/create', methods=['POST'])
# Create a new announcementc
def create_announcement():
    data = request.get_json()
    title = data['title']
    content = data['content']
    datetime = data['datetime']
    is_publish = data['is_publish']
    announcement = Announcement(title=title, content=content, date=datetime, is_publish=is_publish)
    db.session.add(announcement)
    db.session.commit()
    return {'message': 'OK'}, 200

@app.route('/api/announcement/update', methods=['POST'])
def update_announcement():
    data = request.get_json()
    id = data['id']
    title = data['title']
    content = data['content']
    datetime = data['datetime']
    is_publish = data['is_publish']
    try:
        announcement = Announcement.query.filter_by(id=id).first()
        announcement.title = title
        announcement.content = content
        announcement.date = datetime
        announcement.is_publish = is_publish
        db.session.commit()
        return {'message': 'OK'}, 200
    except:
        return {'message': 'Failed!'}, 404


# @login_required
@app.route('/api/announcement/getall', methods=['GET'])
def get_all_announcement():
    try:
        # query all rows in the table
        info = []
        announcement = Announcement.query.all()
        for i in announcement:
            tmp = {'id': i.id, 'title': i.title, 'content': i.content, 'date': i.date, 'is_publish': i.is_publish}
            info.append(tmp)
        return {'message': 'OK', 'MessageInfo':info}, 200
    except:
        return {'message': 'Failed!'}, 404




@swag_from('swagger/checkticket.yml')
# @login_required
@app.route('/api/checkticket', methods=['POST'])
def check_ticket():
    data = request.get_json()
    key = data['key']
    try:
        ticket = Ticket.query.filter_by(key=key).first()
        if ticket:
            if ticket.label == 1:
                return {'message': 'OK', 'key': ticket.key, 'label': ticket.label,'level':ticket.level}, 200
            else:
                return {'message': 'Used or Expired.', 'key': ticket.key, 'label': ticket.label,'level':ticket.level}, 501
    except:
        return {'message': 'Not Found!'}, 404

@swag_from('swagger/activity_create.yml')
# @login_required
@app.route('/api/activity/create', methods=['POST'])
def create_activity():
    data = request.get_json()
    title = data['title']
    content = data['content']
    specy = data['specy']
    begin_date = data['begin_date']
    end_date = data['end_date']
    num = data['num']
    try:
        activity = Activity(title=title, content=content, specy=specy, begin_date=begin_date, end_date=end_date,num=num)
        db.session.add(activity)
        db.session.commit()
        return {'message': 'OK'}, 200
    except:
        return {'message': 'Failed!'}, 404

@swag_from('swagger/activity_delete.yml')
# @login_required
@app.route('/api/activity/delete', methods=['POST'])
def delete_activity():
    data = request.get_json()
    id = data['id']
    try:
        activity = Activity.query.filter_by(id=id).first()
        db.session.delete(activity)
        db.session.commit()
        return {'message': 'OK'}, 200
    except:
        return {'message': 'Failed!'}, 404

@swag_from('swagger/activity_get.yml')
# @login_required
@app.route('/api/activity/get', methods=['POST'])
def get_activity():
    data = request.get_json()
    id = data['id']
    try:
        activity = Activity.query.filter_by(id=id).first()
        return {'message': 'OK', 'id': activity.id, 'title': activity.title, 'content': activity.content, 'specy': activity.specy, 'begin_date': activity.begin_date, 'end_date': activity.end_date,'num':activity.num}, 200
    except:
        return {'message': 'Not Found!'}, 404

@swag_from('swagger/activity_update.yml')
# @login_required
@app.route('/api/activity/update', methods=['POST'])
def update_activity():
    data = request.get_json()
    id = data['id']
    title = data['title']
    content = data['content']
    specy = data['specy']
    begin_date = data['begin_date']
    end_date = data['end_date']
    num = data['num']
    try:
        activity = Activity.query.filter_by(id=id).first()
        activity.title = title
        activity.content = content
        activity.specy = specy
        activity.begin_date = begin_date
        activity.end_date = end_date
        activity.num = num
        db.session.commit()
        return {'message': 'OK'}, 200
    except:
        return {'message': 'Failed!'}, 404

# @swag_from('swagger/activity.yml')
# @login_required
@app.route('/api/activity/getall', methods=['GET'])
def get_all_activity():
    try:
        # query all rows in the table
        info = []
        activities = Activity.query.all()
        for i in activities:
            tmp = {'id': i.id, 'title': i.title, 'content': i.content, 'specy': i.specy, 'begin_date': i.begin_date, 'end_date': i.end_date,'num':i.num}
            info.append(tmp)
        return {'message': 'OK', 'MessageInfo':info}, 200
    except:
        return {'message': 'Failed!'}, 404

# For test
# @app.route('/api/comment/create', methods=['POST'])
# def create_comment():
#     data = request.get_json()
#     author = data['author']
#     content = data['content']
#     date = data['date']
#     time = data['time']
#     is_forbidden = data['is_forbidden']
#     try:
#         comment = Comment(author=author, content=content, date=date, time=time, is_forbidden=is_forbidden)
#         db.session.add(comment)
#         db.session.commit()
#         # Add author
#         # author_ = Author(name=author, is_forbidden=is_forbidden)
#         # db.session.add(author_)
#         # db.session.commit()
#         return {'message': 'OK'}, 200
#     except:
#         return {'message': 'Failed!'}, 404


@app.route('/api/comment/getall', methods=['GET'])
def get_all_comment():
    try:
        # query all rows in the table
        comment_info = []
        comments = Comment.query.all()
        for i in comments:
            tmp = {'id': i.id, 'author': i.author, 'content': i.content, 'date': i.date, 'date': i.date, 'is_forbidden': i.is_forbidden}
            comment_info.append(tmp)
        author_info = []
        authors = Author.query.all()
        for i in authors:
            tmp = {'id':i.id,'name':i.name,'comments':i.comments,'is_forbidden':i.is_forbidden}
            author_info.append(tmp)
        return {'message': 'OK','CommentInfo':comment_info,'AuthorInfo':author_info}, 200
    except:
        return {'message': 'Failed!'}, 404

@app.route('/api/comment/forbidden', methods=['POST'])
def forbidden_comment():
    try:
        data = request.get_json()
        id = data['id']
        comment = Comment.query.filter_by(id=id).first()
        comment.is_forbidden = True
        db.session.commit()
        return {'message': 'OK'}, 200
    except:
        return {'message': 'Failed!'}, 404

@app.route('/api/comment/forbidden/author', methods=['POST'])
def forbidden_author():
    try:
        data = request.get_json()
        id = data['id']
        author = Author.query.filter_by(id=id).first()
        author.is_forbidden = True
        db.session.commit()
        return {'message': 'OK'}, 200
    except:
        return {'message': 'Failed!'}, 404

if __name__ == '__main__':
    app.run(debug=True)