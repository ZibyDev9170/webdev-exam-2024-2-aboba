import os
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError
from models import db, Book, Genre, Cover, BookGenre, Review
from hashlib import md5
from werkzeug.utils import secure_filename
from markupsafe import Markup, escape
import markdown2


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
    # Добавляем сортировку по дате выхода (год)
    req = db.select(Book).order_by(Book.year.desc())
    if request.args.get('name'):
        req = req.filter(Book.title.ilike(f'%{request.args.get("name")}%'))
    if len(request.args.getlist('genre_ids')):
        req = req.join(Book.genres).filter(Genre.id.in_(request.args.getlist("genre_ids")))

    page = request.args.get('page', 1, type=int)
    pagination = db.paginate(req, page=page, per_page=10)
    books = pagination.items

    genres = db.session.execute(db.select(Genre)).scalars()
    return render_template('books/index.html',
                           books=books,
                           genres=genres,
                           pagination=pagination,
                           search_params=search_params())


@books_bp.route('/new')
@login_required
def new():
    if not (current_user.role_id == 1):
        flash('У вас недостаточно прав для доступа к данной странице!', 'danger')
        return redirect(url_for('books.index'))
    book = Book()
    genres = db.session.execute(db.select(Genre)).scalars()
    return render_template('books/new.html',
                           genres=genres,
                           book=book)

@books_bp.route('/create', methods=['POST'])
@login_required
def create():
    try:
        cover_file = request.files['cover_img']
        cover = None
        if cover_file.filename:
            cover_type = os.path.splitext(cover_file.filename)[-1]
            cover = Cover(
                filename=secure_filename(cover_file.filename),
                mime_type=cover_file.mimetype,
                md5_hash=md5(cover_file.read()).hexdigest()
            )
            existing_cover = db.session.execute(db.select(Cover).where(Cover.md5_hash == cover.md5_hash)).scalar()
            if existing_cover:
                cover = existing_cover
            else:
                db.session.add(cover)
                db.session.commit()
                cover_file.seek(0)
                cover_file.save(f'{current_app.config["UPLOAD_FOLDER"]}/{cover.id}{cover_type}')
        
        book_params = params()
        if cover:
            book_params['cover_id'] = cover.id
        book = Book(**book_params)
        db.session.add(book)
        db.session.commit()

        genre_ids = request.form.getlist('genre_ids')
        for genre_id in genre_ids:
            book_genre = BookGenre(book_id=book.id, genre_id=genre_id)
            db.session.add(book_genre)
        db.session.commit()

        flash(f'Книга была успешно добавлена!', 'success')
        return redirect(url_for('books.index'))
    except IntegrityError as e:
        db.session.rollback()
        genres = db.session.execute(db.select(Genre)).scalars()
        flash(f'Не заполнены все поля для корректного отображения книги.', 'danger')
        return render_template('books/new.html', genres=genres, book=book)



@books_bp.route('/<int:book_id>/edit')
@login_required
def edit(book_id):
    if not (current_user.role_id == 1 or current_user.role_id == 2):
        flash('У вас недостаточно прав для доступа к данной странице!', 'danger')
        return redirect(url_for('books.index'))
    book = db.get_or_404(Book, book_id)
    genres = db.session.execute(db.select(Genre)).scalars()
    return render_template('books/edit.html', book=book, genres=genres)

@books_bp.route('/<int:book_id>/update', methods=['POST'])
@login_required
def update(book_id):
    book = db.get_or_404(Book, book_id)
    params_ = params()
    try:
        for param, item in params_.items():
            if item == None:
                raise IntegrityError
        book.title = params_['title']
        book.description = params_['description']
        book.year = params_['year']
        book.publisher = params_['publisher']
        book.author = params_['author']
        book.pages = params_['pages']
        db.session.commit()
        genre_ids = request.form.getlist('genre_ids')
        if len(genre_ids) > 0:
            db.session.execute(db.delete(BookGenre).where(BookGenre.book_id == book.id))
            print(genre_ids)
            for genre_id in genre_ids:
                book_genre = BookGenre(book_id=book.id, genre_id=genre_id)
                db.session.add(book_genre)
            db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash('Не удалось обновить книгу.', 'danger')
        return redirect(url_for('books.edit', book_id=book.id))

    flash('Книга была успешно обновлена!', 'success')
    return redirect(url_for('books.show', book_id=book.id))

@books_bp.route('/<int:book_id>/delete', methods=['POST'])
@login_required
def delete(book_id):
    if not (current_user.role_id == 1):
        flash('У вас недостаточно прав для удаления книги!', 'danger')
        return redirect(url_for('books.index'))
    book = db.get_or_404(Book, book_id)
    try:
        db.session.delete(book)
        db.session.commit()
        flash('Книга была успешно удалена!', 'success')
    except IntegrityError:
        db.session.rollback()
        flash('Не удалось удалить книгу.', 'danger')

    return redirect(url_for('books.index'))

@books_bp.route('/<int:book_id>/show')
def show(book_id):
    book = db.get_or_404(Book, book_id)
    img = db.get_or_404(Cover, book.cover_id)
    user_review = None
    if current_user.is_authenticated:
        user_review = db.session.execute(db.select(Review).where(Review.book_id == book_id, Review.user_id == current_user.id)).scalar()

    page = request.args.get('page', 1, type=int)
    per_page = 6
    reviews_query = db.select(Review).where(Review.book_id == book_id)
    pagination = db.paginate(reviews_query, page=page, per_page=per_page)
    reviews = pagination.items

    return render_template('books/show.html', book=book, user_review=user_review, cover=img, reviews=reviews, pagination=pagination)

@books_bp.route('/<int:book_id>/review', methods=['GET', 'POST'])
@login_required
def review(book_id):
    book = db.get_or_404(Book, book_id)
    existing_review = db.session.execute(db.select(Review).where(Review.book_id == book_id, Review.user_id == current_user.id)).scalar()
    
    if existing_review:
        flash('Вы уже писали рецензию на эту книгу.', 'danger')
        return redirect(url_for('books.show', book_id=book_id))

    if request.method == 'POST':
        rating = request.form.get('rating')
        text = request.form.get('text')
        if not rating or not text:
            flash('Все поля обязательны для заполнения.', 'danger')
            return render_template('books/review.html', book=book)

        sanitized_text = Markup(escape(text)).unescape()
        html_text = markdown2.markdown(sanitized_text)
        review = Review(book_id=book_id, user_id=current_user.id, rating=rating, text=html_text)
        db.session.add(review)
        db.session.commit()
        
        book.rating_count += 1
        book.rating_sum += int(rating)
        db.session.commit()

        flash('Ваша рецензия была успешно добавлена!', 'success')
        return redirect(url_for('books.show', book_id=book_id))

    return render_template('books/review.html', book=book)

@books_bp.route('/<int:book_id>/review/<int:review_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_review(book_id, review_id):
    review = db.get_or_404(Review, review_id)
    if not (current_user.role_id in [1, 2] or current_user.id == review.user_id):
        flash('У вас недостаточно прав для доступа к данной странице!', 'danger')
        return redirect(url_for('books.show', book_id=book_id))

    if request.method == 'POST':
        review.rating = request.form.get('rating')
        text = request.form.get('text')
        html_text = markdown2.markdown(Markup(escape(text)).unescape())
        review.text = html_text
        db.session.commit()
        flash('Ваша рецензия была успешно обновлена!', 'success')
        return redirect(url_for('books.show', book_id=book_id))

    return render_template('books/edit_review.html', review=review, book_id=book_id)

@books_bp.route('/<int:book_id>/review/<int:review_id>/delete', methods=['POST'])
@login_required
def delete_review(book_id, review_id):
    review = db.get_or_404(Review, review_id)
    if not (current_user.role_id in [1, 2] or current_user.id == review.user_id):
        flash('У вас недостаточно прав для доступа к данной странице!', 'danger')
        return redirect(url_for('books.show', book_id=book_id))

    db.session.delete(review)
    db.session.commit()

    book = db.get_or_404(Book, book_id)
    book.rating_count -= 1
    book.rating_sum -= review.rating
    db.session.commit()

    flash('Рецензия была успешно удалена!', 'success')
    return redirect(url_for('books.show', book_id=book_id))
