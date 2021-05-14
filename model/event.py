from ._init_ import db

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    date = db.Column(db.String(50))
    location = db.Column(db.String(50))
    price = db.Column(db.Integer)
    complete = db.Column(db.Boolean)
    user_id = db.Column(db.Integer)
    created = db.Column(db.DateTime, server_default=db.func.now())
    updated = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())