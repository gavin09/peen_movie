from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from indexer import Indexer
from datetime import datetime

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
    if not indexer.forward_index.has_key(query):
        indexer.create_index(indexer.raw_data, query)
    search_results = indexer.get_index(query, 'all')
    return render_template("search_results.html", query=query, search_results=search_results)

if __name__ == '__main__':
    indexer = Indexer()

    #date = datetime.today()
    #date_str = date.strftime('%Y%m%d')
    indexer.load_data_from_file("data", "20150520.txt")
    app.run(debug=True)
