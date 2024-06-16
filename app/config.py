import os

class Config:
    SECRET_KEY = '6342eb430febed6def4d4063a2fa717907fb4911143de1891c59dca9e0519bd8'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///library.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media', 'images')
