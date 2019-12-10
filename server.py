from flask import Flask, render_template, flash, request, redirect
from wtforms import Form, validators, StringField, IntegerField

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '8e9ea5751c9a42f284e1782af5acb7d9'


class ReusableForm(Form):
    alpha = IntegerField('Alpha', validators=[validators.optional()])
    input_text = StringField('InputText', validators=[validators.data_required()])


@app.route("/", methods=['GET', 'POST'])
def index():
    form = ReusableForm(request.form)
    data = dict()

    if request.method == 'POST':
        alfa = request.form['alpha']
        input_text = request.form['input_text']

        if form.validate():
            # procesari
            flash('Eroare: text eroare.')
        else:
            flash('Campul text este obligatoriu.')

    return render_template('home.html', form=form, data=data)


@app.route("/instructions", methods=['GET', 'POST'])
def instructions():
    return render_template('instructions.html')


@app.errorhandler(404)
def page_not_found(e):
    return redirect('/')


if __name__ == "__main__":
    app.run()
