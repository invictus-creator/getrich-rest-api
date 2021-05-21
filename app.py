import os
from flask import Flask
from flask_restful import Api
# from flask_jwt import JWT
from resources.transaction import Transaction, RecentTransactions, TransactionsInCategory
from resources.category import Category, CategoryList
# from security import authenticate, identify
# from resources.user import UserRegister

app = Flask(__name__)
db_url = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("://", "ql://", 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.secret_key = "secret1"
api = Api(app)

# jwt = JWT(app, authenticate, identify)

api.add_resource(Transaction, '/transaction')
api.add_resource(RecentTransactions, '/recenttransactions')
api.add_resource(TransactionsInCategory, '/transactionsincategory')
api.add_resource(Category, '/category')
api.add_resource(CategoryList, '/categorylist')
api.add_resource(Notification, '/notification')
api.add_resource(NotificationList, '/notificationlist')
# api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from db import db

    db.init_app(app)
    app.run(debug=True)
