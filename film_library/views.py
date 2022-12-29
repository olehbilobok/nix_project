import datetime
import uuid
import secrets
import os
from flask import Flask, render_template, flash, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegistrationForm, LoginForm, CreateFilmForm, EditFilmForm, EditProfileForm, SearchForm
from flask_login import LoginManager, login_user, logout_user, current_user, login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = '_y2b#-m(nwf8irkpgs)wpg+-e$#_7^xaevp^me4+u4ov+3fyw*'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/flaskdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)

from models import *


@login_manager.user_loader
def load_user(user_id):
    return CustomUser.query.get(int(user_id))


@app.route('/')
def home():
    return render_template('home.html', title='Home')


@app.route('/register', methods=['GET', 'POST'])
def sign_up():
    form = RegistrationForm()
    if form.validate_on_submit():
        user_email = CustomUser.query.filter_by(email=form.email.data).first()
        user_username = CustomUser.query.filter_by(username=form.username.data).first()

        if user_email:
            flash('Email address already exists!', 'error')
            return redirect(url_for('sign_up'))
        if user_username:
            flash('Username already exists!', 'error')
            return redirect(url_for('sign_up'))

        new_user = CustomUser(username=form.username.data, email=form.email.data,
                              password=generate_password_hash(form.password.data, method='sha256'))
        db.session.add(new_user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = CustomUser.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login Ivalid. Please check email or password')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/film', methods=['GET'])
def get_films():

    page = request.args.get('page', 1, type=int)
    films = Film.query.order_by(Film.release.desc()).paginate(page=page, per_page=10)

    return render_template('films/all_films.html', films=films)


def save_poster(form_poster):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_poster.filename)
    poster_name = random_hex + f_ext
    poster_path = os.path.join(app.root_path, 'static/poster_pics', poster_name)
    form_poster.save(poster_path)
    return poster_name


@app.route('/film/new', methods=['GET', 'POST'])
@login_required
def create_film():
    form = CreateFilmForm()
    if form.validate_on_submit():
        film_name = Film.query.filter_by(name=form.name.data).first()

        if film_name:
            flash('Film already exists!', 'error')
            return redirect(url_for('create_film'))

        poster_file = save_poster(form.poster.data) if form.poster.data else 'default.png'

        form_director = form.director.data.split(' ')
        db_director = Director.query.filter_by(last_name=form_director[1]).first()

        if not db_director:
            created_director_id = uuid.uuid4().hex[:5]
            new_director = Director(id=created_director_id, first_name=form_director[0], last_name=form_director[1])
            db.session.add(new_director)
            db.session.commit()

            new_film = Film(name=form.name.data, genre=form.genre.data, release=form.release.data,
                            description=form.description.data, rating=form.rating.data, poster=poster_file,
                            user_id=current_user.id, director_id=created_director_id)

            db.session.add(new_film)
            db.session.commit()
            flash('Film created!', 'success')
            return redirect(url_for('get_films'))

        else:
            new_film = Film(name=form.name.data, genre=form.genre.data, release=form.release.data,
                            description=form.description.data, rating=form.rating.data, poster=poster_file,
                            user_id=current_user.id, director_id=db_director.id)

            db.session.add(new_film)
            db.session.commit()
            flash('Film created!', 'success')
            return redirect(url_for('get_films'))

    return render_template('films/create_film.html', form=form)


@app.route('/film/my', methods=['GET', 'POST'])
@login_required
def my_films():
    page = request.args.get('page', 1, type=int)
    films = Film.query.filter_by(user_id=current_user.id).order_by(Film.release.desc()).paginate(page=page, per_page=10)
    return render_template('films/my_films.html', films=films)


@app.route('/film/<int:film_id>')
def get_film(film_id):
    film = Film.query.get_or_404(film_id)
    return render_template('films/get_film.html', film=film)


@app.route('/film/my/<int:film_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_film(film_id):
    film = Film.query.get_or_404(film_id)
    form = EditFilmForm()
    if form.validate_on_submit():
        director = Director.query.filter_by(id=film.director_id).first()

        poster_file = save_poster(form.poster.data) if form.poster.data else film.poster
        form_director = form.director.data.split(' ')

        director.first_name = form_director[0]
        director.last_name = form_director[1]
        db.session.commit()

        film.name = form.name.data
        film.genre = form.genre.data
        film.release = form.release.data
        film.description = form.description.data
        film.rating = form.rating.data
        film.poster = poster_file
        film.director_id = film.director_id
        db.session.commit()

        flash('Your film\'s info has been updated')
        return redirect(url_for('edit_film', film_id=film.id))

    if request.method == "GET":
        form.name.data = film.name
        form.genre.data = film.genre
        form.release.data = film.release
        form.description.data = film.description
        form.rating.data = film.rating
        form.poster.data = film.poster
        form.director.data = f"{film.directors.first_name} {film.directors.last_name}"

    return render_template('films/edit_film.html', form=form)


@app.route('/film/my/<int:film_id>', methods=['POST'])
@login_required
def delete_film(film_id):
    film = Film.query.get_or_404(film_id)
    db.session.delete(film)
    db.session.commit()
    flash('Film has been deleted', 'success')
    return redirect(url_for('my_films'))


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def my_profile():
    customuser = CustomUser.query.get(current_user.id)
    form = EditProfileForm()

    if form.validate_on_submit():
        customuser.username = form.username.data
        customuser.email = form.email.data
        db.session.commit()
        flash('Your personal info has been updated', 'success')
        return redirect(url_for('my_profile'))

    if request.method == "GET":
        form.username.data = customuser.username
        form.email.data = customuser.email

    return render_template('my_profile.html', form=form)


@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)


@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        page = request.args.get('page', 1, type=int)
        films = Film.query.filter(Film.name.like('%' + form.name.data + '%')).order_by(Film.release.desc()).\
            paginate(page=page, per_page=10)

        return render_template('search.html', form=form, films=films)


@app.route('/filter/my', defaults={'route': 'my'},  methods=['GET', 'POST'])
@app.route('/filter/all', defaults={'route': 'all'}, methods=['GET', 'POST'])
def filter_films(**kwargs):

    r = request.args
    page = r.get('page', 1, type=int)
    genre = r.get('genre')
    release_date_from = r.get('release_date_from')
    release_date_to = r.get('release_date_to')
    director = r.get('director')

    films = Film.query

    if director and kwargs.get('route') == 'all':
        films = films.join(Director).filter(Director.last_name.like(director))

    if director and kwargs.get('route') == 'my':
        films = films.join(Director).filter(CustomUser.id == current_user.id, Director.last_name.like(director))

    if genre and kwargs.get('route') == 'all':
        films = films.filter(Film.genre.like(genre))

    if genre and kwargs.get('route') == 'my':
        films = films.join(CustomUser).filter(CustomUser.id == current_user.id, Film.genre.like(genre))

    if release_date_from and kwargs.get('route') == 'all' or release_date_to and kwargs.get('route') == 'all':
        from_ = release_date_from if release_date_from else datetime.date(1900, 1, 1)
        to_ = release_date_to if release_date_to else datetime.date(2100, 1, 1)

        films = films.filter(
            and_(
                Film.release >= from_,
                Film.release <= to_
            )
        )

    if release_date_from and kwargs.get('route') == 'my' or release_date_to and kwargs.get('route') == 'my':
        from_ = release_date_from if release_date_from else datetime.date(1900, 1, 1)
        to_ = release_date_to if release_date_to else datetime.date(2100, 1, 1)

        films = films.join(CustomUser).filter(CustomUser.id == current_user.id,
                                              (and_(Film.release >= from_, Film.release <= to_)))

    films = films.paginate(page=page, per_page=10)

    return render_template('filter.html', films=films, genre_parm=genre, from_parm=release_date_from,
                           to_parm=release_date_to, director_parm=director)


@app.route('/order/my', defaults={'route': 'my'}, methods=['GET', 'POST'])
@app.route('/order/all', defaults={'route': 'all'}, methods=['GET', 'POST'])
def order_films(**kwargs):
    page = request.args.get('page', 1, type=int)
    rating = request.args.get('rating')
    release = request.args.get('release')

    films = Film.query

    if rating and kwargs.get('route') == 'all':
        films = films.order_by(Film.rating.desc())

    if rating and kwargs.get('route') == 'my':
        films = films.join(CustomUser).filter(CustomUser.id == current_user.id).order_by(Film.rating.desc())

    if release and kwargs.get('route') == 'all':
        films = films.order_by(Film.release.desc())

    if release and kwargs.get('route') == 'my':
        films = films.join(CustomUser).filter(CustomUser.id == current_user.id).order_by(Film.rating.desc())

    films = films.paginate(page=page, per_page=10)

    return render_template('order.html', films=films, rating_parm=rating,
                           release_parm=release)


if __name__ == '__main__':
    app.run(port=8000, debug=True)
