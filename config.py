import projet
from pathlib import Path
import os

from flask import Flask, app

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = '#d#JCqTTW\nilK\\7m\x0bp#\tj~#H'

PROJET_ID = 1200420960103822

MEDIA_ROOT= BASE_DIR / 'static/images'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    'C:/Users/chaimae/Documents/master S3/Analysis, mining & indexing in big multimedias systems/projet/projet/static',
]