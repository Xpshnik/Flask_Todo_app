from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(100))
    completed = db.Column(db.Boolean)


db.create_all()

@app.get('/')
def todo_list():
    todo_list = db.session.query(Todo).all()
    return render_template('todo_list.html', todo_list=todo_list)


@app.post('/add')
def add_task():
    task_name = request.form.get('task_name')
    new_todo = Todo(task_name=task_name, completed=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('todo_list'))


@app.get('/update/<int:todo_id>')
def update_task(todo_id):
    todo = db.sesson.query(Todo).filter(Todo.id == todo_id).first()
    todo.completed = not todo.completed
    db.session.commit()
    return redirect(url_for('todo_list'))


@app.get('/delete/<int:todo_id>')
def delete_task(todo_id):
    todo = db.session.query(Todo).filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('todo_list'))
