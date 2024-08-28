# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

#instance of api
app = Flask(__name__)
# app.db will be created when we do `flask db init`
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

# instance that allows us to migrate models into sql db (app.db)
migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add routes here
@app.route('/earthquakes/<int:id>')
def get_earthquake_by_id(id):
    q = Earthquake.query.filter_by(id=id).first()
    # checking if query did not find anything (q is None)
    if(not q):
        return {'message': f'Earthquake {id} not found.'}, 404
    #SerializerMixing allows us to use .to_dict()
    return jsonify(q.to_dict()), 200

@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_earthquake_by_mag(magnitude):
    #return a list of Earthquake instances
    q = Earthquake.query.filter(Earthquake.magnitude>=magnitude).all()
    #turning each Earthquake instance into a dictionary (so that we can jsonify it)
    #.to_dict() is available thanks to SerializerMixin (see models.py)
    q_dict = [quake.to_dict() for quake in q]
    ret_json = {
        #manually creating the "count" field
        "count": len(q_dict),
        "quakes": q_dict
    }
    return jsonify(ret_json), 200
    


if __name__ == '__main__':
    app.run(port=5555, debug=True)
