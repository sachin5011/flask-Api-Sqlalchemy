from extensions.sqlalchemy_extensions import db

class Employee(db.Model):
    emp_id = db.Column(db.Integer, primary_key=True)
    emp_name = db.Column(db.String(150))
    emp_email = db.Column(db.String(150))
    avatar = db.Column(db.String(350))



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    email = db.Column(db.String(200))
    phone = db.Column(db.String(200))
    role = db.Column(db.String(200))
    password = db.Column(db.String(200))
    avatar = db.Column(db.String(200))
    role_id = db.Column(db.Integer)


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    roles = db.Column(db.String(200))


class Endpoint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    endpoints = db.Column(db.String(250))
    method = db.Column(db.String(100))







