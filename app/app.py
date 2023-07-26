import json
from flask import Flask, make_response, request, jsonify
from flask_cors import CORS
import functools
from mapper import sqlite_mapper as sql

app = Flask(__name__)
CORS(app,
     origins=['http://localhost:8182', 'yourserver domain'],
     methods=['OPTIONS', 'GET', 'POST'])


def authentication():

    def auth(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not request.headers.get('some-custome-header') == 'some token':
                return jsonify('error'), 400
            return func(*args, **kwargs)

        return wrapper

    return auth


@app.route('/twi-archiver', methods=['GET', 'POST'])
@authentication()
def archiver():
    res = jsonify('success')
    if request.method == 'POST':
        sql.delins(request.json)
    if request.method == 'GET':
        res = jsonify(sql.select(10))
    return res, 200


@app.route('/twi-archiver/all', methods=['GET'])
@authentication()
def getall():
    return jsonify(sql.selectall()), 200


@app.route('/twi-archiver/show', methods=['GET'])
def show():
    did = request.args.get('divid', 'A')
    num = '10'
    try:
        num = str(int(str(request.args.get('lim', 10))))
    except:
        pass
    return """
<div id=""" + did + """></div><script>
(($)=>{localStorage.setItem($,a=localStorage.getItem($)||prompt``);
fetch(`${origin}/${$}/render?divid=""" + did + """&lim=""" + num + """`,{headers:{'Content-Type':'application/json',[$]:a}}).then(r=>r.json()).then(eval)
})($='twi-archiver')</script>
        """, 200


@app.route('/twi-archiver/render', methods=['GET'])
@authentication()
def renderer():
    did = request.args.get('divid', 'A')
    num = 10
    try:
        num = int(str(request.args.get('lim', 10)))
    except:
        pass
    javascript = """
document.body.style.backgroundColor='black'
JSON.parse(""" + json.dumps(sql.select(num)) + """).map(v => {
div=document.createElement('div')
div.dataset.rowid=v.rowid
div.dataset.category=v.category
bq=document.createElement("blockquote")
bq.className="twitter-tweet"
bq.dataset.theme="dark"
a=document.createElement("a")
a.href=`https://twitter.com/_/status/${v.tweetid}?ref_src=twsrc%5Etfw`
bq.appendChild(a)
div.appendChild(bq)
""" + did + """.appendChild(div)
""" + did + """.style.display='flex'
""" + did + """.style.flexWrap='wrap'
})
sc=document.createElement("script")
sc.async=true
sc.src="https://platform.twitter.com/widgets.js"
sc.charset="utf-8"
""" + did + """.append(sc)
    """
    return jsonify(javascript), 200


# TODO how update category? cron?

if __name__ == ('__main__'):
    sql.create()
    app.run(host='0.0.0.0', port=8182, debug=False)
