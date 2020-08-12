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

    print(start)
    print(stop)
    print(left)
    print(right)

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


# @app.route("/parse_gen")
# def parser2():
#     """Parsing left right and urls range"""
#     urls = request.args.get('url').strip()
#     urls = re.split(r"[ \n]", str(urls))
#
#     out = "Processing links:"
#     for i, u in enumerate(urls):
#         out += f"<p>{i:>03}: {u}</p>"
#         start_spider.delay(url=u)
#     return f"<div classname=result>{out}</div>"


if __name__ == "__main__":
    app.run(debug=True)
