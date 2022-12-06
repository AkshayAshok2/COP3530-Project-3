from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

@app.route("/<name>")
def home(name):
    return render_template("test.html", content=["time", "to", "go"])

# @app.route('/')
# def my_form():
#     return render_template('my_form.html')

# @app.route('/', methods=['POST'])
# def my_form_post():
#     characters = request.form['characters'] # Gets list of characters
#     keywords = request.form['keywords'] # Gets word/phrase for search
#     return 'Hello'

if __name__ == '__main__':
    app.run()