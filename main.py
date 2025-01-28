from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
Bootstrap5(app)

# CREATE DB

class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
db.init_app(app)

# CREATE TABLE
class Movie(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True)
    year: Mapped[int]
    description: Mapped[str]
    rating: Mapped[float]
    ranking: Mapped[int]
    review: Mapped[str]
    img_url: Mapped[str]


with app.app_context():
    db.create_all()


# with app.app_context():
#     new_movie = Movie(
#         title = "Phone Booth",
#         year = 2002,
#         description = """
# Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down
# by an extortionist's sniper rifle. Unable to leave or receive outside help,
# Stuart's negotiation with the caller leads to a jaw-dropping climax.
# """,
#         rating = 7.3,
#         ranking = 10,
#         review = "My favourite character was the caller.",
#         img_url = "https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
#     )

#     db.session.add(new_movie)
#     db.session.commit()


@app.route("/")
def home():
    movies = db.session.execute(db.select(Movie).order_by(Movie.title)).scalars()
    return render_template("index.html", movies = movies)


if __name__ == '__main__':
    app.run(debug=True)
