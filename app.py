# Backend app for the Admin system
# Based on Flask
# Note : Not Under Testing Yet

from flask import Flask, request, render_template, redirect, url_for, session, flash
from flasgger import swag_from, Swagger
from models.model import Admin, Notice, Activity, Ticket
from login_required import login_required
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:bzx20020814@localhost:3306/mydb3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db=SQLAlchemy(app)
Swagger(app)

# Create the routes
@app.route('/')
def index():
    return {'message': 'Hello, World!'}, 200

@swag_from('swagger/login.yml')
@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'POST':
            # Check if the input adminname and password is in the database
            adminname = request.form['username']
            password = request.form['password']
            admin = Admin.query.filter_by(adminname=adminname).first()
            if admin:
                if password == admin.password:
                    session['id'] = admin.id
                    return redirect(url_for('admin'))
                else:
                    flash('Wrong password!')
            else:
                flash('Admin not found!')
        else:
            return {'message': 'OK'}, 200
    except KeyError:
        return {'message': 'Not Found'}, 404
       

# @login_required
# @app.route('/admin')
# def admin():
#     # According to the admin's authority, unlock the corresponding function
#     # admin = Admin.query.filter_by(id=session['id']).first()
#     # if admin.authority == 'super':
#     # return render_template('admin.html') 
#     return    


# @login_required
@swag_from('swagger/logout.yml')
@app.route('/logout')
def logout():
    session.pop('id', None)
    return redirect(url_for('index'))

# TODO...
# @login_required
# @app.route('/api/sessiontype', methods=['POST'])
# def sessiontype():
#     data = request.get_json()
#     type = data['t_type']

# @login_required
# @app.route('/api/txtpagesession', methods=['POST'])
# def txtpagesession():
#     data = request.get_json()\
#     page = data['page']


# @login_required
@swag_from('swagger/announcement.yml')
@app.route('/api/deletetxt', methods=['POST'])
# Delete an announcement
def delete_annoucement():
    data = request.get_json()
    id = data['id']
    try:
        notice = Notice.query.filter_by(id=id).first()
        db.session.delete(notice)
        db.session.commit()
        return {'message': 'OK'}, 200
    except:
        return {'message': 'Not Found'}, 404

# @swag_from('swagger/announcement.yml')
@login_required
@app.route('/api/gettxt', methods=['POST'])
# Get the content of an announcement
def get_annoucement():
    data = request.get_json()
    id = data['id']
    try:
        notice = Notice.query.filter_by(id=id).first()
        return {'message': 'OK', 'title': notice.title, 'content': notice.content}, 200
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
    notice = Notice(title=title, content=content)
    db.session.add(notice)
    db.session.commit()
    return {'message': 'OK'}, 200

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
                return {'message': 'Ok', 'key': ticket.key, 'label': ticket.label}, 200
            else:
                return {'message': 'Used or Expired.', 'key': ticket.key, 'label': ticket.label}, 501
    except:
        return {'message': 'Not Found!'}, 404

@swag_from('swagger/activity_create.yml')
# @login_required
@app.route('/api/activity/create', methods=['POST'])
def create_activity():
    data = request.get_json()
    id = data['id']
    title = data['title']
    content = data['content']
    specy = data['specy']
    begin_date = data['begin_date']
    end_date = data['end_date']
    try:
        activity = Activity(id=id, title=title, content=content, specy=specy, begin_date=begin_date, end_date=end_date)
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
        return {'message': 'Not Found'}, 404

@swag_from('swagger/activity_get.yml')
# @login_required
@app.route('/api/activity/get', methods=['POST'])
def get_activity():
    data = request.get_json()
    id = data['id']
    try:
        activity = Activity.query.filter_by(id=id).first()
        return {'message': 'OK', 'title': activity.title, 'content': activity.content, 'specy': activity.specy, 'begin_date': activity.begin_date, 'end_date': activity.end_date}, 200
    except:
        return {'message': 'Not Found'}, 404

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
    try:
        activity = Activity.query.filter_by(id=id).first()
        activity.title = title
        activity.content = content
        activity.specy = specy
        activity.begin_date = begin_date
        activity.end_date = end_date
        db.session.commit()
        return {'message': 'OK'}, 200
    except:
        return {'message': 'Failed!'}, 404

# @swag_from('swagger/activity.yml')
# @login_required
@app.route('/api/activity/getall', methods=['POST'])
def get_all_activity():
    try:
        activity = Activity.query.all()
        return {'message': 'OK', 'activity': activity}, 200
    except:
        return {'message': 'Not Found'}, 404







if __name__ == '__main__':
    app.run(debug=True)