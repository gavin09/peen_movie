from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from indexer import Indexer

app = Flask(__name__)
Bootstrap(app)
indexer = Indexer()
indexer.load_data_from_file("20150428", "data.txt")

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
    query_utf8 = query.encode('utf-8')
    if not indexer.forward_index.has_key(query_utf8):
        indexer.create_index(indexer.raw_data, query_utf8)
    search_results = indexer.get_index(query_utf8, 'all')
    return render_template("search_results.html", query=query, search_results=search_results)

if __name__ == '__main__':
    app.run(debug=True)
