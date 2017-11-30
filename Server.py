from flask import Flask, request
from flask.ext.restful import inputs
from flask.ext.restful import reqparse
from flask.ext.restful import marshal, Api, Resource

FLASK_SERVER_NAME = 'https://api.github.com/repos/slimanir/REST-Service-System'

app = Flask(__name__)
api = Api(app)
class Server(Resource):
	def get(self):
		s= Server.query.get()
		if not s:
			abort(404)
		return s
api.add_resource(Server, '/repos')
	def post(self):
		args = parser.parse_args()
		s=Server(**args)

		db.session.add(s)
		db.commit()
		return s
api.add_resource(Server, '/repos')

	errors = { 'NotFoundError':{'message':'Not found','status':404,}'FrobnitzError': ...,}
api = Api(app, errors=errors)

if __name__ == "__main__":
    app.run()
