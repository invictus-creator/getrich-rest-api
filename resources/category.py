# from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from models.category import CategoryModel
from models.transaction import TransactionModel
from db import db


class Category(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id',
                        type=str,
                        required=False)
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank.")
    parser.add_argument('type',
                        type=str,
                        required=True,
                        help="This field cannot be left blank.")
    parser.add_argument('budget',
                        type=float,
                        required=False,
                        default=0.0)

    # @jwt_required()
    def get(self):
        data = Category.parser.parse_args()
        category = CategoryModel.find_by_name(data['name'].lower())

        if category:
            return category.json(), 200
        else:
            return {"message": "Category not found."}, 404

    # @jwt_required()
    def post(self):
        data = Category.parser.parse_args()
        data = {"name": data['name'].lower(), "type": data['type'].lower(), "budget": data['budget']}

        if CategoryModel.find_by_name(data['name'].lower()):
            return {"message": "A category with that name already exists."}, 400

        category = CategoryModel(**data)

        try:
            category.save_to_db()
        except:
            return {"message": "An error occurred inserting the category."}, 500

        return category.json(), 201

    # @jwt_required()
    def delete(self):
        data = Category.parser.parse_args()

        category = CategoryModel.find_by_name(data['name'].lower())
        if category:
            db.session.query(TransactionModel).filter(TransactionModel.category == data['name']).delete()
            category.delete_from_db()

        return {"message": "Category and associated transactions deleted."}

    # @jwt_required()
    def put(self):
        data = Category.parser.parse_args()
        data = {"name": data['name'].lower(), "type": data['type'].lower(), "budget": data['budget']}

        category = CategoryModel.find_by_name(data['name'].lower())

        if category is None:
            category = CategoryModel(**data)
        else:
            # if the type has been changed, update prices in transaction table
            if not category.type == data['type']:
                category.type = data['type']
                TransactionModel.update_prices(**data)

        category.save_to_db()
        return category.json()


class CategoryList(Resource):
    def get(self):
        return {"category list": [category.json() for category in CategoryModel.query.all()], }


