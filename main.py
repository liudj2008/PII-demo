import secrets

import jwt
from flask import Flask
from flask_restx import Resource, Api, fields

from Api.tokenize import tokenize
from Redis.redis import Redis
from Authorization.auth_middleware import token_required
app = Flask(__name__)
api = Api(
    app=app,
    doc='/docs',
    version='1.0.0',
    title='Incognito API',
    description='PII data API demo'
)

input_fields = api.model('Resource', {})

input_field_login = api.model('UserId', {
    'user_id': fields.Integer()
})

# init Redis and tokens
conn = Redis()
conn.set()

# Generate urlsafe secret key
app.config["SECRET_KEY"] = secrets.token_urlsafe(16)


@api.route('/login', methods=['POST'])
class Login(Resource):
    @api.expect(input_field_login)
    def post(self):
        return jwt.encode(api.payload, app.config["SECRET_KEY"], algorithm="HS256")


@api.route('/tokenize', methods=['POST'])
class Tokenize(Resource):
    @api.expect(input_fields)
    @token_required
    def post(self, current_user):
        response = []

        for item in api.payload['input']:
            data_category = item['data_category']
            data = item['data']
            data_tokenized = tokenize(conn, data_category, data, reverse=False)
            response.append({
                'data_category': data_category,
                'data': data_tokenized
            })
        return response


@api.route('/detokenize', methods=['POST'])
class DeTokenize(Resource):
    @api.expect(input_fields)
    @token_required
    def post(self, current_user):
        response = []

        for item in api.payload['input']:
            data_category = item['data_category']
            data = item['data']
            data_detokenized = tokenize(conn, data_category, data, reverse=True)
            response.append({
                'data_category': data_category,
                'data': data_detokenized
            })
        return response


# main driver function
if __name__ == '__main__':
    app.run(port=8080, debug=True)
