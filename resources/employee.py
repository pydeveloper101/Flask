from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.employee import EmployeeModel
from models.company import CompanyModel


class Employee(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('salary',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('company',
                        type=str,
                        required=True,
                        help="Every employee needs a company."
                        )

    @jwt_required
    def get(self, name):
        employee = EmployeeModel.find_by_name(name)
        if employee:
            return employee.json()
        return {'message': 'Item not found'}, 404

    def post(self,name):

        if EmployeeModel.find_by_name(name):
            return {'message':'Already Exists'}

        data = Employee.parser.parse_args()
        company = CompanyModel.find_by_name(data['company'])
        if not company:
            return {'message':'Company Does not exist'}

        employee = EmployeeModel(name, **data)


        try:
            employee.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500


    def delete(self,name):
        employee = EmployeeModel.find_by_name(name)

        if employee:
            employee.delete_from_db(self)
            return {'message':'Employee Deleted'}
        return {'message':'Employee Does not exist'}

    def put(self, name):
        data = Employee.parser.parse_args()

        employee = EmployeeModel.find_by_name(name)

        if employee:
            employee.salary = data['price']
        else:
            employee = EmployeeModel(name, **data)

        employee.save_to_db()

        return employee.json()


class EmployeeList(Resource):
    def get(self):
        return {'items': list(map(lambda x: x.json(), EmployeeModel.query.all()))}