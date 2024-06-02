import fastapi
import json
import logging
from data_trafic.service_output import Rulon_output, List_of_rulons
from data_trafic.rulon import Rulon
import sqlalchemy
from sqlalchemy.orm import sessionmaker, declarative_base
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import uvicorn
import datetime
import pytz

def checker(column):
    match column:
        case "Id": return Rulon.rulon_id
        case "length": return Rulon.length
        case "weight": return Rulon.weight
        case "date_of_insert": return Rulon.date_of_insert
        case "date_of_delete": return Rulon.date_of_delete

def list_tables(engine):
    inspector = sqlalchemy.inspect(engine)
    table_names = inspector.get_table_names()
    return table_names

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
app = fastapi.FastAPI()

engine = sqlalchemy.create_engine('sqlite:///DB_for_rulon.db')
tables = list_tables(engine)
logger.info(f"{tables}")
Session =  sessionmaker(bind=engine)
session = Session()
logger.info(f"Сервис чист")


@app.get("/filter")
def filter_table(column:str, from_filter, to_filter, stat: bool):
    column_check=checker(column)
    if not stat:
        rulons=[Rulon_output(id=int(rulon.rulon_id),
                            length=float(rulon.length),
                            weight=float(rulon.weight),
                            date_of_insert=(rulon.date_of_insert),
                            date_of_delete=rulon.date_of_delete if rulon.date_of_delete else datetime.datetime(1000, 1, 1, 1, 1, 1, 100000))
                for rulon in session.query(Rulon).filter(column_check.between(from_filter, to_filter)).all()]
        service_output = List_of_rulons(list_output=rulons)
        service_output_json = service_output.model_dump(mode="json")
        with open("output_json.json", "w") as output_file:
            json.dump(service_output_json, output_file, indent=4)
        return JSONResponse(content=jsonable_encoder(service_output_json))
    else:
        count_insert=session.query(sqlalchemy.func.count(Rulon.rulon_id)).filter(column_check.between(from_filter, to_filter)).scalar()
        count_delete=session.query(sqlalchemy.func.count(Rulon.rulon_id)).filter(column_check.between(from_filter, to_filter), Rulon.date_of_delete.isnot(None)).scalar()
        avg_length=session.query(sqlalchemy.func.avg(Rulon.length)).filter(column_check.between(from_filter, to_filter)).scalar()
        avg_weight=session.query(sqlalchemy.func.avg(Rulon.weight)).filter(column_check.between(from_filter, to_filter)).scalar()
        min_length=session.query(sqlalchemy.func.min(Rulon.length)).filter(column_check.between(from_filter, to_filter)).scalar()
        min_weight=session.query(sqlalchemy.func.min(Rulon.weight)).filter(column_check.between(from_filter, to_filter)).scalar()
        max_length=session.query(sqlalchemy.func.max(Rulon.length)).filter(column_check.between(from_filter, to_filter)).scalar()
        max_weight=session.query(sqlalchemy.func.max(Rulon.weight)).filter(column_check.between(from_filter, to_filter)).scalar()
        sum_weight=session.query(sqlalchemy.func.sum(Rulon.weight)).filter(column_check.between(from_filter, to_filter)).scalar()
        logger.info(f"{count_insert}")
        logger.info(f"{count_delete}")
        logger.info(f"{avg_length}")
        logger.info(f"{avg_weight}")
        logger.info(f"{min_length}")
        logger.info(f"{min_weight}")
        logger.info(f"{max_length}")
        logger.info(f"{max_weight}")
        logger.info(f"{sum_weight}")
        mass_id = [rulon.rulon_id for rulon in session.query(Rulon.rulon_id).filter(column_check.between(from_filter, to_filter), Rulon.date_of_delete.isnot(None)).all()]
        date_diff=[]
        for id in mass_id:
            #logger.info(id)
            rulon=session.query(Rulon).get(id)
            date_del=getattr(rulon, "date_of_delete")
            date_ins=getattr(rulon, "date_of_insert")
            logger.info(date_del-date_ins)
            date_diff.append(date_del-date_ins)
        logger.info(max(date_diff))
        logger.info(min(date_diff))

        #logger.info(f"{date_diff}")
        return {"count_insert": count_insert, "count_delete": count_delete, "avg_length":avg_length, "avg_weight":avg_weight , "min_length":min_length , "min_weight":min_weight,
                "max_length":max_length , "max_weight":max_weight , "sum_weight":sum_weight , "date_max": max(date_diff), "date_min": min(date_diff)}


@app.get("/warehouse")
def warehouse():
    if not engine.connect():
        return {"Error": "Ошибка соединения"}
    rulons=[Rulon_output(id=int(rulon.rulon_id),
                         length=float(rulon.length),
                         weight=float(rulon.weight),
                         date_of_insert=(rulon.date_of_insert),
                         date_of_delete=rulon.date_of_delete if rulon.date_of_delete else datetime.datetime(1000, 1, 1, 1, 1, 1, 100000))
            for rulon in session.query(Rulon).filter(Rulon.date_of_delete.is_(None)).all()]
    service_output = List_of_rulons(list_output=rulons)
    service_output_json = service_output.model_dump(mode="json")
    with open("output_json.json", "w") as output_file:
        json.dump(service_output_json, output_file, indent=4)
    return JSONResponse(content=jsonable_encoder(service_output_json))

@app.get("/delete")
def delete_row(id: int):
    row=session.query(Rulon).get(id)
    date_del=getattr(row, "date_of_delete")
    logger.info(date_del)
    if not date_del:
        row.date_of_delete=datetime.datetime.now(pytz.timezone("Europe/Moscow"))
        session.commit()
        return f"{row.rulon_id},{row.length},{row.weight},{row.date_of_insert},{row.date_of_delete}"
    else:
        return "Уже удалено со склада"


@app.get("/insert")
def insert_data(length: int, weight: int):
    right_now=datetime.datetime.now(pytz.timezone("Europe/Moscow"))
    new_rulon = Rulon(length=length, weight=weight, date_of_insert=right_now)
    session.add(new_rulon)
    session.commit()
    return "Успех"

@app.get("/all/")
def get_all() -> JSONResponse:

    if not engine.connect():
        return {"Error": "Ошибка соединения"}
    rulons=[Rulon_output(id=int(rulon.rulon_id),
                         length=float(rulon.length),
                         weight=float(rulon.weight),
                         date_of_insert=(rulon.date_of_insert),
                         date_of_delete=rulon.date_of_delete if rulon.date_of_delete else datetime.datetime(1000, 1, 1, 1, 1, 1, 100000))
            for rulon in session.query(Rulon).all()]
    service_output = List_of_rulons(list_output=rulons)
    service_output_json = service_output.model_dump(mode="json")
    with open("output_json.json", "w") as output_file:
        json.dump(service_output_json, output_file, indent=4)
    return JSONResponse(content=jsonable_encoder(service_output_json))

uvicorn.run(app, host="localhost", port=7000)
