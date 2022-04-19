import secrets
from random import randint
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from forms import TodoForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = secrets.token_hex(randint(1, 100))
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(300))
    is_urgent = db.Column(db.Boolean)
    is_completed = db.Column(db.Boolean)


db.create_all()

@app.get('/')
def todo_list():
    task_list = db.session.query(Todo).all()
    form = TodoForm()
    return render_template('todo_list.html', todo_list=task_list, form=form)


@app.post('/add')
def add_task():
    form = TodoForm(request.form)
    if form.validate_on_submit():
        task_name = request.form.get('task_name')
        is_urgent = bool(request.form.get('is_urgent'))
        new_todo = Todo(task_name=task_name, is_urgent=is_urgent, is_completed=False)
        db.session.add(new_todo)
        db.session.commit()
        flash(f'A new task successfully created!', 'success')
        return redirect(url_for('todo_list'))
    else:
        todo_list = db.session.query(Todo).all()
        return render_template('todo_list.html', todo_list=todo_list, form=form)


@app.get('/update/<int:todo_id>')
def update_task(todo_id):
    todo = db.session.query(Todo).filter(Todo.id == todo_id).first()
    todo.is_completed = not todo.is_completed
    db.session.commit()
    return redirect(url_for('todo_list'))


@app.get('/delete/<int:todo_id>')
def delete_task(todo_id):
    todo = db.session.query(Todo).filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('todo_list'))
