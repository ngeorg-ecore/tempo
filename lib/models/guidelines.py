import datetime
from extensions import db

# Aliases
Column = db.Column
Integer = db.Integer
String = db.String
Datetime = db.DateTime
Float = db.Float


class Model(db.Model):

    __tablename__ = "parent_table"
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    date_registered = Column(Datetime)
    time_registered = Column(String)

    def __init__(self, **kwargs):

        # Execute prefunctions if any
        self.prefunctions()

        # If values are in there, attrib, else don't.
        if kwargs:
            print(f"{self.__class__.__name__} Created")
            for k, v in kwargs.items():
                setattr(self, k, v)

        # Standard values
        self.date_registered = datetime.date.today()
        self.time_registered = datetime.datetime.now()

        # Commit and Save the register, even if empty
        db.session.add(self)
        db.session.commit()

        # Execute postfunctions if any
        self.postfunctions()

    def prefunctions(self):
        """overwrite"""

    def postfunctions(self):
        """overwrite"""

    def update(self, **kwargs):
        if kwargs:

            for key, value in kwargs.items():
                setattr(self, key, value)

            db.session.add(self)
            db.session.commit()

        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def re_fetch(self):
        self.postfunctions()