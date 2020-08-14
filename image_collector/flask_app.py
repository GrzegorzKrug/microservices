from flask import Flask, request, render_template
from image_collector.tasks import start_spider
from image_collector.celery import app as cel_app
import re

# import requests

app = Flask(__name__)


def get_task_stats():
    i = cel_app.control.inspect()

    active = 0
    queue = 0

    act = i.active()
    for key, val in act.items():
        active += len(val)

    que = i.reserved()
    for key, val in que.items():
        queue += len(val)

    return active, queue


@app.route("/")
def index():
    page = render_template("CreateTask.html")
    act, que = get_task_stats()
    page += f"<p>Active: {act}</p>"
    page += f"<p>Queue: {que}</p>"
    return page


# @app.route("/tasks")
# def tasks():
#     print("Loading tasks que")
#     page = ""
#     # print(dir(cel_app.control.inspect))
#     act, que = get_task_stats()
#     page += f"<p>Active: {act}</p>"
#     page += f"<p>Queue: {que}</p>"
#     return page


@app.route("/show_urls")
def show_urls():
    page = render_template("CreateTask.html")

    # urls = request.args.get('url').strip()
    # urls = re.split(r"[ \n]", str(urls))
    start = request.args.get('first')
    stop = request.args.get('last')
    left = request.args.get('left')
    right = request.args.get('right')

    out = "Generated urls:"

    for url, error in generate_urls(start, stop, left, right):
        out += f"<p>{url}</p>"

    page += out
    return page


def generate_urls(start, stop, left, right):
    try:
        start = int(start)
        stop = int(stop)
        if start > stop:
            start, stop = stop, start

    except ValueError as ve:
        yield f"invalid parameter: {ve}", True

    except TypeError as err:
        yield f"empty parameter: {err}", True
    else:
        for num in range(start, stop + 1):
            yield f"{left}{num}{right}", False


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
            out += f" {er}"
        out += "</p>"
    return f"<div classname=result>{out}</div>"


@app.route("/parser2")
def parser2():
    start = request.args.get('first')
    stop = request.args.get('last')
    left = request.args.get('left')
    right = request.args.get('right')

    out = "Parsing urls:"
    for cur_url, error in generate_urls(start, stop, left, right):
        try:
            if not error:
                start_spider.delay(url=cur_url)
            else:
                out += f"<p>{cur_url}</p>"
        except Exception as er:
            print(f"{er}")
            out += f"<p>{cur_url} {er}</p>"
        else:
            out += f"<p>{cur_url}</p>"

    return out


if __name__ == "__main__":
    app.run(host='0.0.0.0')
