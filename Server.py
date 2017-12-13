from flask import Flask, request, jsonify
from flask.ext.restful import inputs
from flask.ext.restful import reqparse
from flask.ext.restful import marshal, Api, Resource
from time import *
from pygit2 import Repository, clone_repository

FLASK_SERVER_NAME = 'https://api.github.com/repos/slimanir/REST-Service-System'

app = Flask(__name__)
api = Api(app)
results = []
todo = 0

class Server(Resource):
	def get(self):
		s= Server.query.get()
		if not s:
			abort(404)
		return s
api.add_resource(Server, '/repo')
	def post(self):
		args = parser.parse_args()
		s=Server(**args)

		db.session.add(s)
		db.commit()
		return s
api.add_resource(Server, '/repo')

	errors = { 'NotFoundError':{'message':'Not found','status':404,}'FrobnitzError': ...,}
api = Api(app, errors=errors)

def set_repo():
    try:
        repo = Repository('./repo')
    except:
        repo_url = 'FLASK_SERVER_NAME'
        repo_path = './repo'
        repo = clone_repository(repo_url, repo_path)
    return repo

def get_commits(repo):
    commits = []
    for commit in repo.walk(repo.head.target):
        commits.append(repo.get(commit.id))
    return commits

@app.route('/work' , methods=['GET'])
def task():
    repo = set_repo()
    commits = get_commits(repo)
   

    try:
        commit_hash = commits[todo]
        todo += 1
        end_time = time() - start_time
        print(end_time)
        return jsonify({'commit': str(commit_hash.id), 'id': todo})
    except:
        return None

@app.route('/results', methods=['POST'])
def store_result():
    results.append(request.json)
    return 'Task Completed'

if __name__ == "__main__":
    app.run()
    start_time = time()
