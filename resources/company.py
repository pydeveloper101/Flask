from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.company import CompanyModel


class Company(Resource):

    def get(self,name):
        company = CompanyModel.find_by_name(name)
        if company:
            return company.json()
        return {'message':'company does not exist'},400

    def post(self, name):
        if CompanyModel.find_by_name(name):
            return {'message': "A store with name '{}' already exists.".format(name)}, 400

        company = CompanyModel(name)
        try:
            company.save_to_db()
        except:
            return {"message": "An error occurred creating the store."}, 500

        return company.json(), 201


    def delete(self, name):
        company = CompanyModel.find_by_name(name)
        if company:
            company.delete_from_db()

        return {'message': 'Store deleted'}


class CompanyList(Resource):
    def get(self):
        return {'companies': list(map(lambda x: x.json(), CompanyModel.query.all()))}