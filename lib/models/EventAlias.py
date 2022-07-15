from lib.models.guidelines import Integer, Column, Model, String


class EventAlias(Model):

    __bind_key__ = "persistency"
    __tablename__ = "event_alias"

    match = Column(String)
    issue_key = Column(String)
