from flask import request
from werkzeug.utils import redirect

from bp.database import database_bp
from extensions import db

from lib.models.CalendarEvent import CalendarEvent
from lib.models.SeniorRegister import SeniorRegister


@database_bp.route("/create_database/<mode>")
def create_database(mode):
    if mode == "hard":
        # Create
        db.drop_all()
        db.create_all()

    if mode == "soft":
        # Create
        db.drop_all(bind=None)
        db.create_all()

    return redirect("/log_time")


@database_bp.post("/edit/<model>/<id>")
def edit_single_field(model, id):
    datatypes = {
        "str": str,
        "int": int,
        "float": float
    }

    models = {
        "calendar_event": CalendarEvent,
        "senior_register": SeniorRegister
    }

    payload = request.json

    if 'values' in payload.keys():
        print(payload['values'])
        for value in payload['values']:
            register = models[model].query.filter_by(id=value['id']).first()
            key = value['key']
            value = datatypes[value['dtype']](value['value'])
            setattr(register, key, value)
            register.save()

        return {"status_code": 200, "extra": ["nothing"]}

    else:
        register = models[model].query.filter_by(id=id).first()
        key = payload['key']
        value = datatypes[payload['dtype']](payload['value'])
        setattr(register, key, value)
        register.save()

        if model == "calendar_event":
            if key == "issue_key":
                register.postfunctions()

        return {"status_code": 200, "extra": ["nothing"]}
