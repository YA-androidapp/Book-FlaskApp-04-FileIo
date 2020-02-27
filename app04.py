from flask import Flask, make_response
import logging

app = Flask(__name__)


# app.logger.setLevel(logging.DEBUG)


# LOGFILE = 'app.log'
# LOGFORMAT = '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
# fileHandler = logging.FileHandler(LOGFILE)
# fileHandler.setLevel(logging.DEBUG)
# formatter = logging.Formatter(LOGFORMAT)
# fileHandler.setFormatter(formatter)
# app.logger.addHandler(fileHandler)


@app.route('/')
def index():
    app.logger.debug('A value for debugging')
    app.logger.warning('A warning occurred (%d apples)', 42)
    app.logger.error('An error occurred')
    return make_response('logging', 400)