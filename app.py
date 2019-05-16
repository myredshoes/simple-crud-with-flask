import os

from flask import Flask
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask import redirect


project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "bookdatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)


class Book(db.Model):
    title = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    author = db.Column(db.String(80), unique=False, nullable=False, index=True)

    def __repr__(self):
        return "<Title: {}>".format(self.title), "<Author: {}>".format(self.author)


@app.route("/", methods=["GET", "POST"])
def home():
    books = None
    if request.form:
        try:
            book = Book(title=request.form.get("title"), author=request.form.get("author"))
            db.session.add(book)
            db.session.commit()
        except Exception as e:
            print("Failed to add item")
            print(e)
    books = Book.query.all()
    return render_template("home.html", books=books)


@app.route("/update", methods=["POST"])
def update():
    try:
        newtitle = request.form.get("newtitle")
        oldtitle = request.form.get("oldtitle")
        newauthor = request.form.get("newauthor")
        oldauthor = request.form.get("oldauthor")
        book = Book.query.filter_by(title=oldtitle, author=oldauthor).first()
        book.title = newtitle
        book.author = newauthor
        db.session.commit()
    except Exception as e:
        print("Couldn't update item title")
        print(e)
    return redirect("/")


@app.route("/delete", methods=["POST"])
def delete():
    title = request.form.get("title")
    author = request.form.get("author")
    book = Book.query.filter_by(title=title, author=author).first()
    db.session.delete(book)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
