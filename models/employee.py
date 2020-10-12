from db import db
from models.company import CompanyModel


class EmployeeModel(db.Model):
    __tablename__ = 'employees'
    id  = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    salary = db.Column(db.Float(precision=2))
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    company = db.relationship('CompanyModel')

    def __init__(self,name,salary,company):
        self.salary = salary
        self.name = name

        self.company_id = CompanyModel.query.filter_by(name=company)[0].id


    @classmethod
    def find_by_name(cls, name):
        print('_----------------------------------')
        print(cls.query.all())
        for i in cls.query.filter_by(name=name):
            print(i.name)

        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_company_id_emp(cls,company):
        return CompanyModel.query.filter_by(name=company)



    def json(self):
        return {'name': self.name, 'salary': self.salary,'company':self.company_id}


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()




