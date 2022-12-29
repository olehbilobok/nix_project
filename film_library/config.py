import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = '_y2b#-m(nwf8irkpgs)wpg+-e$#_7^xaevp^me4+u4ov+3fyw*'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost/flaskdb'


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True