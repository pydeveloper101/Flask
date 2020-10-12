from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from db import db
from resources.employee import Employee,EmployeeList
from resources.company import Company,CompanyList
from resources.user import UserRegister
app = Flask(__name__)

POSTGRES = {
    'user': 'postgres',
    'pw': 'ashish',
    'db': 'employee_management',
    'host': 'localhost',
    'port': '5432',
}
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'ayush'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity)  # /auth

api.add_resource(Company, '/company/<string:name>')
api.add_resource(CompanyList, '/companies')
api.add_resource(Employee, '/employee/<string:name>')
api.add_resource(EmployeeList, '/employees')
api.add_resource(UserRegister,   '/register')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)


