from flask import Flask, render_template, send_from_directory
from flask_migrate import Migrate
from models import db, Cover, Genre
from config import Config
from books import books_bp
from auth import auth_bp, init_login_manager

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

init_login_manager(app)

app.register_blueprint(auth_bp)
app.register_blueprint(books_bp)


@app.route('/')
def index():
    genres = Genre.query.all()
    return render_template('index.html', genres=genres)


@app.route('/images/<image_id>')
def image(image_id):
    img = db.get_or_404(Cover, image_id)
    return send_from_directory(app.config['UPLOAD_FOLDER'], img.filename)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
