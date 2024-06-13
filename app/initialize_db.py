from app import app
from models import db, Genre, Role, User
from werkzeug.security import generate_password_hash

def initialize_db():
    with app.app_context():
        db.create_all()

        # Add Genres
        genres = [
            Genre(name='Романтика'),
            Genre(name='Комедия'),
            Genre(name='Детектив'),
            Genre(name='Приключение')
        ]
        db.session.add_all(genres)
        db.session.commit()

        # Add Roles
        roles = [
            Role(name='Администратор', description='Суперпользователь, имеет полный доступ к системе, в том числе к созданию и удалению книг'),
            Role(name='Модератор', description='Может редактировать данные книг и производить модерацию рецензий'),
            Role(name='Пользователь', description='Может оставлять рецензии')
        ]
        db.session.add_all(roles)
        db.session.commit()

        # Add Users
        users = [
            User(
                username='admin',
                password_hash=generate_password_hash('adminpass'),
                last_name='Иванов',
                first_name='Иван',
                middle_name='Иванович',
                role=roles[0]  # администратор
            ),
            User(
                username='moderator',
                password_hash=generate_password_hash('modpass'),
                last_name='Петров',
                first_name='Петр',
                middle_name='Петрович',
                role=roles[1]  # модератор
            ),
            User(
                username='user',
                password_hash=generate_password_hash('userpass'),
                last_name='Сидоров',
                first_name='Сидор',
                middle_name='Сидорович',
                role=roles[2]  # пользователь
            )
        ]
        db.session.add_all(users)
        db.session.commit()

if __name__ == '__main__':
    initialize_db()
