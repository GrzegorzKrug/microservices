from flask import Flask, request
import time
# import requests

app = Flask(__name__)


@app.route("/")
def index():
    pag = "<div>Main Page</div>"
    return pag


@app.route("/hello")
def hello():
    pag = "<div>Hello word</div>"
    return pag


@app.route("/members/<string:name>/")
def get_member(name):
    return name


@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    processed_text = text.upper()
    for x in range(10):
        time.sleep(1)
    print(f"text: '{processed_text}'")

    return processed_text


if __name__ == "__main__":
    app.run(debug=True)
