from flask import Flask
from flask_restx import Resource, Api, fields

from Api.tokenize import tokenize
from Redis.redis import Redis

app = Flask(__name__)
api = Api(
    app=app,
    doc='/docs',
    version='1.0.0',
    title='Incognito API',
    description='PII data API demo'
)

input_fields = api.model('Resource', {
    'data_category': fields.String(),
    'data': fields.Nested(api.model('data', {
        'ssn': fields.String(),
        'address': fields.String()
    }))
})

# init Redis and tokens
conn = Redis()
conn.set()


@api.route('/tokenize', methods=['POST'])
class Tokenize(Resource):
    @api.expect(input_fields)
    def post(self):
        data_category = api.payload['data_category']
        data = api.payload['data']
        return tokenize(conn, data_category, data, reverse=False)


@api.route('/detokenize', methods=['POST'])
class DeTokenize(Resource):
    @api.expect(input_fields)
    def post(self):
        data_category = api.payload['data_category']
        data = api.payload['data']
        return tokenize(conn, data_category, data, reverse=True)


# main driver function
if __name__ == '__main__':
    app.run(port=8080, debug=True)
