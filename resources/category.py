import sqlite3
from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from models.category import CategoryModel
from models.transaction import TransactionModel


class Category(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank.")
    parser.add_argument('_type',
                        type=str,
                        required=True,
                        help="This field cannot be left blank.")

    @jwt_required()
    def get(self):
        data = Category.parser.parse_args()
        category = CategoryModel.find_by_name(data['name'])

        if category:
            return category.json(), 200
        else:
            return {"message": "Category not found."}, 404

    @jwt_required()
    def post(self):
        data = Category.parser.parse_args()

        if CategoryModel.find_by_name(data['name']):
            return {"message": "A category with that name already exists."}, 400

        category = CategoryModel(**data)

        try:
            category.save_to_db()
        except:
            return {"message": "An error occurred inserting the category."}, 500

        return category.json(), 201

    # @jwt_required()
    # def delete(self):
    #     data = Category.parser.parse_args()
    #
    #     conn = sqlite3.connect('data.db')
    #     cur = conn.cursor()
    #
    #     query = "DELETE FROM Categories WHERE category=?"
    #     cur.execute(query, (data['name'],))
    #
    #     conn.commit()
    #     conn.close()
    #
    #     return {"message": "Category deleted."}

    @jwt_required()
    def put(self):
        data = Category.parser.parse_args()

        category = CategoryModel.find_by_name(data['name'])

        if category is None:
            category = CategoryModel(**data)
        else:
            category.type = data['_type']
            TransactionModel.update_prices(**data)

        category.save_to_db()
        return category.json()


class CategoryList(Resource):
    def get(self):
        return {"category list": [category.json() for category in CategoryModel.query.all()]}
