from flask import Flask, Blueprint
from flask_restx import Api, Resource, fields
from flask_restx import fields
import pymongo as pymongo

client = pymongo.MongoClient(
    "mongodb+srv://kekas:kekmasterpassword@cluster0.jhqzb.mongodb.net/marketplace?retryWrites=true&w=majority")
db = client['marketplace']

app = Flask(__name__)
app.config.SWAGGER_UI_DOC_EXPANSION = 'list'
blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint)

app.register_blueprint(blueprint)

company = api.model('Company', {
    'id': fields.Integer(readOnly=True),
    'company': fields.String(),
    'category': fields.Integer(),
    'verification': fields.Integer(),
    'own': fields.Integer(),
    'days_online': fields.Integer(),
})

order = api.model('Order', {
    'id_company': fields.Integer(readOnly=True),
    'delivery_time': fields.Integer(),
    'delivery_cost': fields.Integer(),
    'good': fields.Integer(),
    'bad': fields.Integer(),
    'feedback': fields.Integer(),
    'call': fields.Integer(),
})

product = api.model('Product', {
    'id_company': fields.Integer(readOnly=True),
    'price': fields.Integer(),
    'sale': fields.Integer(),
    'views': fields.Integer(),
})

data = api.model('Data', {
    'companies': fields.List(fields.Nested(company)),
    'orders': fields.List(fields.Nested(order)),
    'products': fields.List(fields.Nested(product)),
})


@api.route('/get-data')
class MyResource(Resource):
    @api.marshal_with(data)
    def get(self):
        global db
        companies = list(db['companies'].find())
        orders = list(db['orders'].find())
        products = list(db['products'].find())
        return {'companies': companies,
                'orders': orders,
                'products': products}
