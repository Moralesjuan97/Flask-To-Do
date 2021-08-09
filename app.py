from flask import Flask, render_template,request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

@app.route('/', methods=['GET'])
def index():
    todos = Todo.query.all()
    return render_template('index.html',todos=todos)

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get("title")
    new_item = Todo(title=title, complete = False)
    db.session.add(new_item)
    db.session.commit()
    return redirect(url_for('index'))
    
@app.route('/complete/<int:todo_id>')
def complete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))
    

if __name__ == "__main__":
    db.create_all()
    
    #create a todo
    # new_item = Todo(title="first task",complete=False)
    # db.session.add(new_item)
    # db.session.commit()
    
    app.run(debug=True)