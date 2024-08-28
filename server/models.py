from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData()

# instance of ORM
db = SQLAlchemy(metadata=metadata)

# Add models here
#SerializerMixin allows us to use .to_dict()
class Earthquake(db.Model, SerializerMixin):
    __tablename__ = "earthquakes" 

    id = db.Column(db.Integer, primary_key=True)
    magnitude = db.Column(db.Float)
    location = db.Column(db.String)
    year = db.Column(db.Integer)

    def __repr__(self):
        return f'<Earthquake {self.id}, {self.magnitude}, {self.location}, {self.year}>'
