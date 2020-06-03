from flask import Flask, jsonify

from takayama.database import init_db, db_session
from takayama.models import Scrobble
from takayama.service import engine

init_db()

app = Flask(__name__)
app.debug = True


@app.route('/')
def hello():
    scrobble = Scrobble.query.first()
    return jsonify(scrobble.serialize)


@app.route('/groupBy/<group_by>/agg/<agg>/filter/<filtering>/limit/<limit>')
def group_agg(group_by, agg, filtering, limit):
    scrobbles = engine(group_by, agg, filtering, limit)
    try:
        result = jsonify(scrobbles)
    except TypeError:
        result = jsonify([s.serialize for s in scrobbles])
    return result


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
