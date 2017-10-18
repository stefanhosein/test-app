import os
import pickle
import language_check
from flask import render_template, flash, redirect
from app import app
from .forms import LoginForm
from .check_text import check_all_errors
from config import DATA_PATH

tool = language_check.LanguageTool('en-US')
model_data = pickle.load(open(os.path.join(DATA_PATH, "gib_model.pki"), "rb"))


@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        msg = check_all_errors(form.response.data, form.exp_response.data, tool, model_data['mat'], model_data['thresh'])
        # msg = "<br>".join(msg.split("\n"))
        flash('Response Given: "%s"' % (form.response.data))
        flash("%s" % msg)
        # flash('Message(s): "%s"' % )
        return redirect('/')
    return render_template('index.html',
                           title='Stefan\'s App',
                           form=form)
