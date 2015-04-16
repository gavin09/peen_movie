from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
Bootstrap(app)

class Search_form(Form):
    query = StringField('query', validators=[DataRequired()])
    search_submit = SubmitField('Search')

@app.route("/", methods=["GET", "POST"])
def homepage():
    form = Search_form(csrf_enabled=False)
    if form.validate_on_submit():
        return redirect(url_for("search_results", query=form.query.data))
    return render_template("home.html", form=form)

@app.route("/search_results/<query>")
def search_results(query):
    return render_template("search_results.html", query=query)

if __name__ == '__main__':
    app.run(debug=True)
