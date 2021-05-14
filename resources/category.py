# from flask_jwt import jwt_required
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
    parser.add_argument('transactions',
                        type=dict,
                        required=False,
                        help="This field cannot be left blank.")

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
        data = {"name": data['name'].lower(), "_type": data['_type'].lower(), "transactions": data['transactions']}

        if CategoryModel.find_by_name(data['name'].lower()):
            return {"message": "A category with that name already exists."}, 400

        l = []
        l.append(data['transactions'])
        data['transactions'] = l
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

        return {"message": "Category and child transactions deleted."}

    # @jwt_required()
    def put(self):
        data = Category.parser.parse_args()
        print("\ndata:", data)
        data = {"name": data['name'].lower(), "_type": data['_type'].lower(), "transactions": data['transactions']}
        print("\ndata after:", data)

        category = CategoryModel.find_by_name(data['name'].lower())

        if category is None:
            # if it's a new category, turn the transaction dict into a list of dicts
            l = []
            l.append(data['transactions'])
            data['transactions'] = l
            category = CategoryModel(**data)
        else:
            transaction = TransactionModel.find_by_id(data['transactions']['id']).json()
            print("\ntransaction:\n", transaction, "\ncategory tx list:\n", category.transactions, "\n\n")
            if transaction is not None:
                # remove it from the category's transactions list, so i can add the updated version, avoid duplicates
                category.delete_transaction(transaction)
            category.transactions.append(data['transactions'])
            print("\ncategory tx list:\n", category.transactions)

            # if the type has been changed, update prices in transaction table
            if not category.type == data['_type']:
                category.type = data['_type']
                TransactionModel.update_prices(**data)

        category.save_to_db()
        return category.json()


class CategoryList(Resource):
    def get(self):
        return {"category list": [category.json() for category in CategoryModel.query.all()],}
