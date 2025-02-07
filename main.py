from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from utils import MovieHandler
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


class EditForm(FlaskForm):
    rating = StringField(
        label="Your rating out of 10.",
        validators=[DataRequired(message="Rating is required.")]
    )
    review = StringField(
        label="Your review",
        validators=[DataRequired(message="Your review is required.")]
    )
    submit = SubmitField("Submit")


class CreateMovieForm(FlaskForm):
    title = StringField(
        label="Movie title",
        validators=[DataRequired(message="Movie title is required.")]
    )
    submit = SubmitField(label="Add movie")



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
    movies = db.session.execute(db.select(Movie).order_by(Movie.rating)).scalars().all()

    for i in range(len(movies)):
        movies[i].ranking = len(movies) - i

    db.session.commit()

    return render_template("index.html", movies = movies)


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    movie = db.get_or_404(Movie, id)
    form = EditForm()
    
    if form.validate_on_submit():
        movie.rating = form.rating.data
        movie.review = form.review.data

        db.session.commit()

        return redirect(url_for('home'))
    
    return render_template("edit.html", movie = movie, form = form)


@app.route("/delete")
def delete():
    movie_id = request.args.get("id")
    movie = db.get_or_404(Movie, movie_id)
    db.session.delete(movie)
    db.session.commit()

    return redirect(url_for("home"))


@app.route("/add", methods = ["GET", "POST"])
def add():
    create_movie_form = CreateMovieForm()
    
    if create_movie_form.validate_on_submit():
        movie_handler = MovieHandler.MovieHandler()
        movies = movie_handler.get_movies(create_movie_form.title.data)

        return render_template("select.html", movies = movies)

    return render_template("add.html", form = create_movie_form)


@app.route("/insert/<int:id>")
def insert(id):
    movie_handler = MovieHandler.MovieHandler()
    selected_movie = movie_handler.get_movie_detail(id)

    new_movie = Movie(
        title = selected_movie.get("title"),
        year = selected_movie.get("release_date")[:4],
        description = selected_movie.get("overview"),
        rating = 0,
        ranking = 0,
        review = "No review yet",
        img_url = f"{movie_handler.img_base_url}{movie_handler.img_poster_ratio}{selected_movie.get("poster_path")}"
    )

    db.session.add(new_movie)
    db.session.commit()

    return redirect(url_for("edit", id = new_movie.id))


if __name__ == '__main__':
    app.run(debug=True)
