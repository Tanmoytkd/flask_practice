from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
ma = Marshmallow(app)


class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(200))
    done = db.Column(db.Boolean)

    def __init__(self, title, description, done):
        self.title = title
        self.description = description
        self.done = done


class ToDoSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description', 'done')


todo_schema = ToDoSchema()
todos_schema = ToDoSchema(many=True)


@app.post('/todo')
def create_todo():
    title = request.json['title']
    description = request.json['description']
    done = False

    todo = ToDo(title, description, done)
    db.session.add(todo)
    db.session.commit()

    return todo_schema.jsonify(todo)


@app.get('/todo')
def get_todos():
    todos = ToDo.query.all()
    return todos_schema.jsonify(todos)


@app.get('/todo/<int:todo_id>')
def get_todo(todo_id):
    todo = ToDo.query.get(todo_id)
    return todo_schema.jsonify(todo)


@app.get('/todo/incomplete')
def get_todo_incomplete():
    todos = ToDo.query.filter_by(done=False).all()
    return todos_schema.jsonify(todos)

@app.get('/todo/completed')
def get_todo_completed():
    todos = ToDo.query.filter_by(done=True).all()
    return todos_schema.jsonify(todos)


@app.put('/todo/<int:todo_id>')
def update_todo(todo_id):
    todo = ToDo.query.get(todo_id)

    todo.title = request.json['title']
    todo.description = request.json['description']
    todo.done = request.json['done']

    db.session.commit()
    return todo_schema.jsonify(todo)


@app.delete('/todo/<int:todo_id>')
def delete_todo(todo_id):
    todo = ToDo.query.get(todo_id)
    db.session.delete(todo)
    db.session.commit()

    return todo_schema.jsonify(todo)


@app.get('/')
def get_root():
    return "Random Data"


@app.get('/hello/<name>')
def get_hello_message(name):
    return f"Hello, {name}!"


@app.post('/hello')
def get_welcome_message():
    name = request.json['name']
    return f"Welcome, {name}!"


if __name__ == '__main__':
    app.run(debug=True)
