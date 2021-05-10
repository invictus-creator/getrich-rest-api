from flask import Flask
from flask_restful import Resource, Api
from flask_jwt import JWT
from resources.transaction import Transaction, RecentTransactions
from resources.category import Category, CategoryList
from security import authenticate, identify
from resources.user import UserRegister
from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "secret1"
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identify)

api.add_resource(Transaction, '/transaction')
api.add_resource(RecentTransactions, '/recenttransactions')
api.add_resource(Category, '/category')
api.add_resource(CategoryList, '/categorylist')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)
