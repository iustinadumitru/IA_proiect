from wtforms import Form, validators, StringField, IntegerField
from flask import Flask, render_template, flash, request, redirect

from processing.main_text_processor import process_text
from collections import defaultdict
from processing import globals

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
        alpha = request.form['alpha']
        input_text = request.form['input_text']

        globals._SCORES = defaultdict(lambda: 0)
        globals.ENUMERATIONS_REMOVED = list()
        globals.NR_LINES_DIALOG_REMOVED = 0
        globals.NR_OF_LINES_SHOWN = 0
        globals.WORD_COUNT = {}
        globals.MAX_SCORE = int(1e9)
        globals.ORIGINAL_TEXT = input_text

        if form.validate():
            output_text, error_message = process_text(input_text, alpha)

            # output_text = ''
            # error_message = "test error"
            # output_text = "test text"
            # error_message = None

            if error_message:
                flash('Eroare: {}.'.format(error_message))

            else:
                data["output_text"] = output_text
                data["lines_removed"] = globals.NR_LINES_DIALOG_REMOVED
                data["enumerations_removed"] = globals.ENUMERATIONS_REMOVED
                data["lines_shown"] = globals.NR_OF_LINES_SHOWN
                data["main_character"] = globals.MAIN_CHARACTER_NAME

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
