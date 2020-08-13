from flask import Flask, request, render_template
from image_collector.tasks import start_spider
import re

# import requests

app = Flask(__name__)


@app.route("/")
def index():
    page = render_template("CreateTask.html")
    return page


@app.route("/show_urls")
def show_urls():
    page = render_template("CreateTask.html")

    # urls = request.args.get('url').strip()
    # urls = re.split(r"[ \n]", str(urls))
    start = request.args.get('first')
    stop = request.args.get('last')
    left = request.args.get('left')
    right = request.args.get('right')
    if start > stop:
        start, stop = stop, start

    try:
        start = int(start)
        stop = int(stop)
    except ValueError as ve:
        return page + f"invalid parameter: {ve}"
    except TypeError as ve:
        return page + f"empty parameter: {ve}"
    out = "Generated urls:"

    for num in range(start, stop + 1):
        out += f"<p>{left}{num}{right}</p>"

    page += out
    return page


# @app.route("/hello")
# def hello():
#     pag = "<div>Hello word</div>"
#     return pag

@app.route("/parser1")
def parser1():
    urls = request.args.get('url').strip()
    urls = re.split(r"[ \n]", str(urls))
    urls = [u for u in urls if len(u) > 10]

    print(urls)
    out = "Processing links:"
    for i, u in enumerate(urls):
        out += f"<p>{i:>03}: {u}"
        try:
            start_spider.delay(url=u)
        except Exception as er:
            print(f"{er}")
            out += f" {ce}"
        out += "</p>"
    return f"<div classname=result>{out}</div>"


@app.route("/parser2")
def parser2():
    start = request.args.get('first')
    stop = request.args.get('last')
    left = request.args.get('left')
    right = request.args.get('right')
    if start > stop:
        start, stop = stop, start

    try:
        start = int(start)
        stop = int(stop)
    except ValueError as ve:
        return f"invalid parameter: {ve}"
    except TypeError as ve:
        return f"empty parameter: {ve}"

    out = "Parsing urls:"
    for num in range(start, stop + 1):
        cur_url = f"{left}{num}{right}"
        start_spider.delay(url=cur_url)
        out += f"<p>{cur_url}</p>"

    return out


if __name__ == "__main__":
    app.run(host='0.0.0.0')
