from pathlib import Path

from flask import Flask, render_template, request, redirect
from models import db, Todo

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///main.db"

db.app = app
db.init_app(app)

# Check if the db file has never been created, create one
if not Path("main.db").is_file():
	db.create_all()

@app.route("/", methods = ["GET", "POST"])
def index_page():
	"""if the request is get list of todos shown otherwise the user
	has used the form to add another todo and will be redirected to index page again
	"""
	if request.method == "POST":
		content = request.form['content']
		db.session.add(Todo(content = content))
		db.session.commit()
		return redirect("/")
	else:
		return render_template("index.html", todos = Todo.query.order_by(Todo.date_created).all())

@app.route("/delete/<int:record_id>")
def delete_page(record_id: int):
    """Delete todo using record_id
    
    Args:
        id (int): The id of todo
    """
    todo_record = Todo.query.get_or_404(record_id)
    db.session.delete(todo_record)
    db.session.commit()
    return redirect("/")

@app.route("/update/<int:record_id>", methods = ["POST", "GET"])
def update_page(record_id: int):
    """Update todo content using record_id
    
    Args:
        record_id (int): The id of todo
    """
    if request.method == "POST":
    	todo = Todo.query.get_or_404(record_id)
    	new_content = request.form["new content"]
    	todo.content = new_content
    	db.session.commit()
    	return redirect("/")
    else:
    	todo = Todo.query.get_or_404(record_id)
    	return render_template("update.html", todo = todo)


if __name__ == "__main__":
	app.run(debug=True)
