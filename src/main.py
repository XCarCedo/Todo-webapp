from pathlib import Path

from flask import Flask, render_template
from models import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///main.db"

db.app = app
db.init_app(app)

# Check if the db file has never been created, create one
if not Path("main.db").is_file():
	db.create_all()

@app.route("/")
def index_page():
	return render_template("index.html")

if __name__ == "__main__":
	app.run(debug=True)