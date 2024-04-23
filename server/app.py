# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

# instance of Flask api
app = Flask(__name__)
# connection to SQLAlchemy ORM's database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

# migration tool to apply SQLAlchemy ORM classes to sqlite database
migrate = Migrate(app, db)
db.init_app(app)

# Earthquake.query.filter(Earthquake.year>1950).all()


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add routes here
@app.route('/earthquakes/<int:earthquake_id>')
def earthquake_by_id(earthquake_id):
    # if no earthquake exists, q will be None
    q = Earthquake.query.filter_by(id=earthquake_id).first()
    if q:
        return make_response(q.to_dict())
    else:
        return make_response({
            'message': f'Earthquake {earthquake_id} not found.'
        }, 404)

@app.route('/earthquakes/magnitude/<float:magnitude>')
def matching_magnitude(magnitude):
    query_result = Earthquake.query.filter(Earthquake.magnitude>=magnitude).all()
    q_list = [e.to_dict() for e in query_result]
    #manually build up rest of JSON response
    return make_response({
        "count": len(q_list),
        "quakes": q_list
    })

if __name__ == '__main__':
    app.run(port=5555, debug=True)
