import os
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError
from models import db, Book, Genre, Cover, BookGenre
from hashlib import md5
from werkzeug.utils import secure_filename

books_bp = Blueprint('books', __name__, url_prefix='/books')

BOOK_PARAMS = [
    'title', 'description', 'year', 'publisher', 'author', 'pages', 'rating_count', 'rating_sum'
]

def params():
    return { p: request.form.get(p) or None for p in BOOK_PARAMS }

def search_params():
    return {
        'name': request.args.get('name'),
        'genre_ids': [x for x in request.args.getlist('genre_ids') if x],
    }

@books_bp.route('/')
def index():
    req = db.select(Book)
    if request.args.get('name'):
        req = req.filter(Book.title.ilike(f'%{request.args.get("name")}%'))
    if request.args.getlist('genre_ids'):
        req = req.join(Book.genres).filter(Genre.id.in_(request.args.getlist("genre_ids")))

    pagination = db.paginate(req)
    books = pagination.items
    genres = db.session.execute(db.select(Genre)).scalars()
    return render_template('books/index.html',
                           books=books,
                           genres=genres,
                           pagination=pagination,
                           search_params=search_params())


@books_bp.route('/new')
# @login_required
def new():
    book = Book()
    genres = db.session.execute(db.select(Genre)).scalars()
    return render_template('books/new.html',
                           genres=genres,
                           book=book)

@books_bp.route('/create', methods=['POST'])
# @login_required
def create():
    try:
        cover_file = request.files['cover_img']
        if cover_file.filename:
            cover_type = os.path.splitext(cover_file.filename)[-1]
            cover = Cover(
                filename=secure_filename(cover_file.filename),
                mime_type=cover_file.mimetype,
                md5_hash=md5(cover_file.read()).hexdigest()
            )
            db.session.add(cover)
            db.session.commit()
        else:
            raise IntegrityError

        book = Book(**params(), cover_id=cover.id)
        db.session.add(book)
        db.session.commit()

        genre_ids = request.form.getlist('genre_ids')
        for genre_id in genre_ids:
            book_genre = BookGenre(book_id=book.id, genre_id=genre_id)
            db.session.add(book_genre)
        db.session.commit()

        cover_file.seek(0)
        cover_file.save(f'{current_app.config["UPLOAD_FOLDER"]}/{cover.id}{cover_type}')
    except IntegrityError:
        db.session.rollback()
        genres = db.session.execute(db.select(Genre)).scalars()
        flash(f'Не заполнены все поля для корректного отображения книги.', 'danger')
        return render_template('books/new.html',
                               genres=genres,
                               book=book)

    flash(f'Книга была успешно добавлена!', 'success')
    return redirect(url_for('books.index'))

@books_bp.route('/<int:book_id>')
def show(book_id):
    book = db.get_or_404(Book, book_id)
    return render_template('books/show.html', book=book)
