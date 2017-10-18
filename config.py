from os.path import join, dirname, realpath

DATA_PATH = join(dirname(realpath(__file__)), 'app/static/data/')
WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'
