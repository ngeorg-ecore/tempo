from lib.models.guidelines import Integer, Column, Model, String


class LoggedOnTempo(Model):
    """
    binded to persistency db

    day = Column(Integer)
    month = Column(Integer)
    year = Column(Integer)

    issue_key = Column(String)
    tempo_worklog_id = Column(Integer)

    """
    __bind_key__ = "persistency"
    __tablename__ = "persistency_tempo_logs"

    day = Column(Integer)
    month = Column(Integer)
    year = Column(Integer)

    issue_key = Column(String)
    tempo_worklog_id = Column(Integer)
