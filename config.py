import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    FLASK_DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hienfi14120s@wsoc03sifne210QQ112024'
    Y_TRANSLATOR_KEY = os.environ.get('Y_TRANSLATOR_KEY')
    ADMINS = ['asimonanm97@gmail.com', 'simonyan.98@mail.com']