import json
from flask import request
from src import app
from .check_text import check_all_errors
from .routes import simple_page


@simple_page.route('/', methods=['POST'])
def check_errors():
    feedback = check_all_errors(request.json['response'], request.json['actual'])
    return json.dumps({"feedback": feedback})

#
# @app.route('/')
# def home():
#     return "Nothing to see here "
