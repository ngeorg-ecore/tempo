import datetime
import json

from lib.functions.get_config import get_config
from lib.functions.get_issue import get_issue
from lib.functions.get_roles_protheus import get_protheus_role
from lib.functions.log_time_on_tempo import log_time_on_tempo
from lib.models.LoggedOnTempo import LoggedOnTempo
from lib.models.guidelines import Model, Column, String, Integer, Datetime


class CalendarEvent(Model):

    __tablename__ = "calendar_event"

    tempo_log_id = Column(Integer)

    year = Column(Integer)
    month = Column(Integer)
    day = Column(Integer)

    original_summary = Column(String)
    issue_key = Column(String)
    description = Column(String)
    billable = Column(Integer, default=0)

    event_date = Column(Datetime)
    google_date = Column(String)
    start_time = Column(String)
    end_time = Column(String)

    is_logged = Column(Integer, default=0) # 0 or 1 if already logged on Tempo
    response = Column(String)

    # Senior
    is_referential = Column(Integer, default=0) # Item below
    reference_type = Column(String)  # [check in], [check out], [lunch time] else "ordinary"

    # Tempo
    original_tempo_datetime = Column(String)
    roles_json = Column(String)
    tempo_role_id = Column(String)
    tempo_role_value = Column(String)

    # From Jira
    original_issue_summary = Column(String)
    original_issue_id = Column(String)

    # link_for_event = Column(String) # TODO V2

    def get_issue(self):
        # Grabs information from issue
        if self.issue_key != "No Issue":
            issue = get_issue(self.issue_key)
            self.update(original_issue_summary=issue['fields']['summary'], original_issue_id=issue['id'])

    def get_roles(self):
        roles_json = get_protheus_role(self.issue_key)

        key = "NONE"
        value = 'None'

        try:
            for role in roles_json['values']:

                if role['key'] != "NONE":
                    key = role['key']
                    value = role['value']
        except:
            pass
        self.update(roles_json=json.dumps(roles_json), tempo_role_id=key, tempo_role_value=value)

    @property
    def roles(self):
        try:
            return json.loads(self.roles_json)["values"]
        except:
            return  []

    def postfunctions(self):
        self.get_issue()
        self.get_roles()

    @property
    def tempo_datetime(self):
        return f"{self.year}-{self.month}-{self.day}T{self.start_time}:00.000"

    @property
    def seconds(self):
        # https://thispointer.com/python-get-difference-between-two-datetimes-in-hours/

        start_hour, start_minute = self.start_time.split(":")
        end_hour, end_minute = self.end_time.split(":")

        start_time = datetime.datetime(2000, 1, 1, int(start_hour), int(start_minute))
        end_time = datetime.datetime(2000, 1, 1, int(end_hour), int(end_minute))

        diff = end_time - start_time
        print(diff)

        return diff.total_seconds()

    def log_this_event(self):
        r = log_time_on_tempo(self.tempo_datetime, self.tempo_role_id, self.seconds, self.description, self.original_issue_id, self.id)
        print(r.status_code, r.text, r.content)
        tempo_log_id = r.json()[0]['tempoWorklogId']
        if r.status_code == 200:
            print("Ok")
            self.update(is_logged=1, response=str(r.status_code) + " - " + r.text, tempo_log_id=tempo_log_id)
            LoggedOnTempo(day=self.day, month=self.month, year=self.year, issue_key=self.issue_key, tempo_worklog_id=tempo_log_id)
            return {"status_code": r.status_code, "message": f"OK [{r.status_code}]"}
        else:
            self.update(response=str(r.status_code) + " - " + r.text)
            return {"status_code": r.status_code, "message": f"Error [{r.status_code}]"}

    def __repr__(self):
        return self.issue_key + " | " + self.description