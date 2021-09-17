from flask import Flask
from flask_restful import Resource, Api, reqparse, abort, marshal_with, fields
from werkzeug.exceptions import BadRequest
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

api = Api(app)

db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'

class TodoModel(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	task = db.Column(db.String(200))
	summary = db.Column(db.String(500))

#db.create_all()


resource_fields = {
	'id' : fields.Integer,
	'task' : fields.String,
	'summary' : fields.String,
}

if __name__ == "__main__":
	app.run(debug = True)

todo_task_args = reqparse.RequestParser()
todo_task_args.add_argument('task', type = str, help = "Task is Required", required = True)
todo_task_args.add_argument('summary', type = str, help = "summary is Required", required = True)

todo_put_args = reqparse.RequestParser()
todo_put_args.add_argument('task', type = str)
todo_put_args.add_argument('summary', type = str)

todo_task_list = {
	1 : {'task': 'write code', 'summary':'will do it'}
}


class all_todos(Resource):
	@marshal_with(resource_fields)
	def get(self):
		task = TodoModel.query.all()
		return task

class todo_task(Resource):
	@marshal_with(resource_fields)
	def get(self,todo_id):

		task = TodoModel.query.filter_by(id = todo_id).first()
		if not task:
			raise BadRequest('Todo ID already does not Exist')
		return task, 200
	
	@marshal_with(resource_fields)
	def post(self,todo_id):
		
		args = todo_task_args.parse_args()
		task = TodoModel.query.filter_by(id = todo_id).first()
		if task:
			raise BadRequest("Todo ID already exsit")

		todo = TodoModel(id = todo_id, task = args['task'], summary = args['summary'])
		db.session.add(todo)
		db.session.commit()
		return todo, 201

	@marshal_with(resource_fields)
	def delete(self,todo_id):
		
		task = TodoModel.query.filter_by(id = todo_id).first()
		if not task:
			raise BadRequest('Todo ID already does not Exist')
		
		db.session.delete(task)
		db.session.commit()
		return 'Todo is Deleted'

	@marshal_with(resource_fields)
	def put(self,todo_id):
		
		put_args = todo_put_args.parse_args()
		task = TodoModel.query.filter_by(id = todo_id).first()

		if not task:
			raise BadRequest('Todo ID already does not Exist')
		
		if put_args['task']:
			task.task = put_args['task']
			

		if put_args['summary']:
			task.summary = put_args['summary']
			
			

		db.session.commit()
		return task
		#return todo_task_list[todo_id]


api.add_resource(todo_task,'/todo_task/<int:todo_id>')
api.add_resource(all_todos,'/todo_task')


@app.route("/")
def hello():
	return "hello world"