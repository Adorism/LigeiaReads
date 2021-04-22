from flask import Flask, render_template, request, jsonify

from flask_wtf import FlaskForm
from wtforms import StringField, TextField, RadioField, SelectMultipleField, SubmitField, SelectField
from wtforms.validators import Required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Galvanizegrad'

class BookRecommend(FlaskForm):
    name = TextField(u'Name')
    words = TextField(u'Pick at Least 3 words')

@app.route('/form', methods=['GET', 'POST'])
def form():
    form = BookRecommend()

    if form.validate_on_submit():
        return '<h1>Alright, {}, prepare for a scare!'.format(form.username.data)
    return render_template('form.html', form=form)

    
if  __name__ == '__main__':
    app.run(debug=True)