from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    is_admin = db.Column(db.Boolean, default=False)

class Leave(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    leave_type = db.Column(db.String(50))
    from_date = db.Column(db.String(10))
    to_date = db.Column(db.String(10))
    reason = db.Column(db.String(200))
    status = db.Column(db.String(20))