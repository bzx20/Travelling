import datetime
from extensions import db

# Create the database model
class Admin(db.Model):
    # Admin of the system
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True,doc='Admin ID')
    adminname = db.Column(db.String(20), unique=True, nullable=False,doc='Admin name')
    password = db.Column(db.String(20), nullable=False,doc='Admin password')
    authority = db.Column(db.String(20), nullable=False,doc='Admin authority')

    def __repr__(self):
        return f"Admin('{self.adminname}', '{self.password}')"

class Notice(db.Model):
    # Notice of activities
    __tablename__ = 'notice'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True,doc='Notice ID')
    title = db.Column(db.String(100), nullable=False,doc='Notice title')
    content = db.Column(db.Text, nullable=False,doc='Notice content')
    # date_start = db.Column(db.DateTime, nullable=False, default=datetime.utcnow,doc='Activity start date')
    # date_end = db.Column(db.DateTime, nullable=False, default=datetime.utcnow,doc='Activity end date')

    # def __repr__(self):
    #     return f"Notice('{self.title}', '{self.content}')"

class Activity(db.Model):
    # Activity of the system
    __tablename__ = 'activity'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True,doc='Activity ID')
    title = db.Column(db.String(100), nullable=False,doc='Activity title')
    content = db.Column(db.Text, nullable=False,doc='Activity content')
    specy = db.Column(db.String(20), nullable=False,doc='Activity specy')
    begin_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow,doc='Activity start date')
    end_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow,doc='Activity end date')

    def __repr__(self):
        return f"Activity('{self.title}', '{self.content}')"

class Ticket(db.Model):
    # Ticket of the system
    __tablename__ = 'ticket'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True,doc='Ticket ID')
    key = db.Column(db.String(20), unique=True, nullable=False,doc='Ticket key')
    label = db.Column(db.Integer, nullable=False,doc='Ticket label')

    def __repr__(self):
        return f"Ticket('{self.key}', '{self.label}')"