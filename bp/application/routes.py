import datetime
import json

from flask import render_template, request, session
from werkzeug.utils import redirect
from bp.application import app_bp
from lib.classes.Automata import Automata
from lib.functions.get_config import get_config
from lib.functions.get_roles_protheus import get_protheus_role
from lib.functions.time_window import time_window
from lib.models.CalendarEvent import CalendarEvent
from lib.models.EventAlias import EventAlias
from lib.models.Inititiative import Initiative
from lib.models.SeniorRegister import SeniorRegister


@app_bp.route("/feed_database", methods=["POST", "GET"])
def feed_database():
    if request.method == "POST":
        payload = request.json

        dates_to_gather = sorted(time_window(**payload))

        # Iterate all days and grabs data
        for date in dates_to_gather:
            Automata().calendar.get_events_for_day(date)

        return {"status_code": 200, "Dates": dates_to_gather}


@app_bp.route("/log_time", methods=["POST", "GET"])
def log_time():
    cfg = get_config()
    pending_registers_from_calendar = CalendarEvent.query.filter_by(is_logged=0).all()
    senior_logs = SeniorRegister.query.filter_by(is_logged=0).all()
    aliases = EventAlias.query.all()
    filtered = {}

    for prfc in pending_registers_from_calendar:

        if prfc.google_date not in filtered.keys():
            filtered[prfc.google_date] = []

        filtered[prfc.google_date].append(prfc)

    today_date = datetime.date.today()

    day = "0" + str(today_date.day) if len(str(today_date.day)) == 1 else str(today_date.day)
    month = "0" + str(today_date.month) if len(str(today_date.month)) == 1 else str(today_date.month)

    today = f"{today_date.year}-{month}-{day}"

    initiatives = Initiative.query.all()
    objects = dict(today=today, initiatives=initiatives, filtered_events=filtered, senior_registers=senior_logs,
                   aliases=aliases, cfg=cfg)
    return render_template("main.html", objects=objects)


@app_bp.post("/log_time_on_tempo")
def tempo_log():
    payload = request.json
    event: CalendarEvent = CalendarEvent.query.filter_by(id=payload['id']).first()
    return event.log_this_event()


@app_bp.post("/delete_event")
def delete_event():
    payload = request.json
    CalendarEvent.query.filter_by(id=payload['id']).first().delete()
    return {"status_code": 200, "message": "deleted"}


@app_bp.post("/get_role")
def get_role():
    payload = request.json
    roles = get_protheus_role(payload['issue_key'])
    event = CalendarEvent.query.filter_by(id=payload['id']).first().update(roles_json=json.dumps(roles))
    print(event)
    return {"original_issue_summary": event.original_issue_summary, "roles": roles}


@app_bp.post("/session/set")
def set_session_key():
    payload = request.json
    session[payload['key']] = payload['value']
    return {"result": f"The key {payload['key']} was set with the value {payload['value']}"}


@app_bp.post("/create_alias")
def create_alias():
    payload = request.json
    EventAlias(**payload)
    return {"status_code": 200, "message": f"Created alias with the following info: {json.dumps(payload)}"}


@app_bp.route("/delete/<obj>/<obj_id>")
def delete_alias(obj, obj_id):
    objects = {
        "alias": EventAlias,
        "initiative": Initiative
    }
    objects[obj].query.filter_by(id=int(obj_id)).first().delete()
    return redirect("/log_time")


@app_bp.post("/add_initiative")
def add_initiative():
    payload = request.json
    Initiative(**payload)
    return {"status_code": 200, "message": "success"}
