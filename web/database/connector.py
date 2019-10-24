from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import DeclarativeMeta
import json
from sqlalchemy.dialects import postgresql


class Manager:
    Base = declarative_base()
    session = None

    def createEngine(self):
        engine = create_engine('postgresql+psycopg2://hglmpvcbmnqequ:6b2d4f95027784aa6c55dc2c2635d417819523416068f2d8ddf186c9d1da48a7@ec2-23-23-173-30.compute-1.amazonaws.com:5432/d2ri8lm7e6ifaf', echo=False)
        self.Base.metadata.create_all(engine)
        return engine

    def getSession(self, engine):
        if self.session == None:
            Session = sessionmaker(bind=engine)
            session = Session()

        return session

class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)
                    fields[field] = data
                except TypeError:
                    fields[field] = None

            return fields

        return json.JSONEncoder.default(self, obj)
