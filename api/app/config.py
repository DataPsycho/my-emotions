import os

basedir = os.path.abspath(os.path.dirname("__file__"))
model_dir = os.path.join(basedir, "modellake")


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dirty_little_secret')
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config_by_name = dict(
    dev=DevelopmentConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY