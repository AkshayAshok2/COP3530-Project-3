import json
from flask import Flask, request, render_template, redirect, url_for, session
import search

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/templates/result.html")
def result():
    return render_template("result.html")

@app.route('/', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        chars = request.form.get('characters')
        keys = request.form.get('keywords')
        kind = request.form.get('search')
        err = int(request.form.get('error'))

        if kind == "Filer":
            kind = True
        else:
            kind = False

        codes, titles, descriptions = search.search(keys, chars, err, kind)
        results = {}
        results['codes'] = codes
        results['titles'] = titles
        results['descriptions'] = descriptions

        with open('results.json', 'w') as file:
            json.dump(results, file)
        return (results, 204)

if __name__ == '__main__':
    app.run(debug=True)