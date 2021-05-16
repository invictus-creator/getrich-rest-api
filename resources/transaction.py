from flask_restful import Resource, reqparse
# from flask_jwt import jwt_required
from models.transaction import TransactionModel
from models.category import CategoryModel


class Transaction(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id',
                        type=str,
                        required=False)
    parser.add_argument('date',
                        type=str,
                        required=True,
                        help="This field cannot be left blank.")
    parser.add_argument('vendor',
                        type=str,
                        required=True,
                        help="This field cannot be left blank.")
    parser.add_argument('category',
                        type=str,
                        required=True,
                        help="This field cannot be left blank.")
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank.")

    # @jwt_required()
    def get(self):
        data = Transaction.parser.parse_args()
        transaction = TransactionModel.find_by_id(data['id'])

        if transaction:
            return transaction.json()
        else:
            return {"message": "Transaction not found."}, 404

    # @jwt_required()
    def post(self):
        data = Transaction.parser.parse_args()

        transaction = TransactionModel(data['date'], data['vendor'].lower(), data['category'].lower(), data['price'])

        try:
            transaction.save_to_db()
        except Exception as e:
            return {"message": f"An error occurred inserting the transaction. {e}"}, 500

        return transaction.json()

    # @jwt_required()
    def put(self):
        data = Transaction.parser.parse_args()

        transaction = TransactionModel.find_by_id(data['id'])

        if transaction is None:
            transaction = TransactionModel(data['date'], data['vendor'].lower(), data['category'].lower(), data['price'])
        else:
            transaction.date = data['date']
            transaction.vendor = data['vendor'].lower()
            transaction.category = data['category'].lower()
            transaction.price = data['price']

        try:
            transaction.save_to_db()
        except:
            return {"message": "An error occurred inserting/updating the transaction."}, 500

        return transaction.json()

    # @jwt_required()
    def delete(self):
        data = Transaction.parser.parse_args()

        transaction = TransactionModel.find_by_id(data['id'])
        if transaction:
            cateogry = CategoryModel.find_by_name(transaction.category)
            cateogry.delete_transaction(transaction=transaction.json())
            transaction.delete_from_db()

        return {"message": "Transaction deleted."}


class RecentTransactions(Resource):
    # @jwt_required()
    def get(self):
        return {"recent": [x.json() for x in TransactionModel.query.order_by(TransactionModel.date.desc(),
                                                                             TransactionModel.id.desc()).limit(50)]}
