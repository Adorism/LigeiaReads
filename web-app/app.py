from flask import Flask, render_template, request, jsonify

from flask_wtf import FlaskForm
from wtforms import widgets, RadioField, SelectMultipleField, SubmitField, SelectField


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Galvanizegraduation'

@app.route('/form')
def form():
    return render_template('form.html')

    
if  __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True, threaded=True)