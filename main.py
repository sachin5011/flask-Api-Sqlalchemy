from flask import Flask
from extensions.sqlalchemy_extensions import db
from controller.employee_controller import emp_api
from controller.user_controller import user_api


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://admin:admin@localhost/adv_works"
db.init_app(app)

with app.app_context():
    db.create_all()


app.register_blueprint(emp_api)
app.register_blueprint(user_api)


if __name__ == '__main__':
    app.run(debug=True)