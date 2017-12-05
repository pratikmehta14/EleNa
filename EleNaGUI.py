import flask
from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash, _app_ctx_stack
import pickle

app = Flask('ElenaApp')

@app.route('/')
def display_initial():
	return render_template('index.html')

@app.route('/dummy', methods=['POST'])
def my_form_post():
	text = request.form['pac-input']
	print text

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
