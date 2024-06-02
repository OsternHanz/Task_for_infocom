import sqlalchemy
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Rulon(Base):
    __tablename__="rulon"

    rulon_id=sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    length=sqlalchemy.Column(sqlalchemy.Float, nullable=False)
    weight=sqlalchemy.Column(sqlalchemy.Float, nullable=False)
    date_of_insert=sqlalchemy.Column(sqlalchemy.DateTime)
    date_of_delete=sqlalchemy.Column(sqlalchemy.DateTime)

#engine = sqlalchemy.create_engine('sqlite:///DB_for_rulon.db')
#declarative_base().metadata.create_all(engine)
engine = sqlalchemy.create_engine('sqlite:///DB_for_rulon.db')
Base.metadata.create_all(engine)
