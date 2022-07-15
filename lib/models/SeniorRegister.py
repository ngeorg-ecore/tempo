from lib.models.guidelines import Model, Column, Datetime, Integer, String


class SeniorRegister(Model):
    __tablename__ = "senior_register"

    weekday = Column(String)
    weekday_number = Column(Integer)
    is_holiday = Column(String)

    entry_1 = Column(String)
    leave_1 = Column(String)
    entry_2 = Column(String)
    leave_2 = Column(String)

    other = Column(String)  # Serialized

    is_logged = Column(Integer, default=0)

    day = Column(Integer)
    month = Column(Integer)
    year = Column(Integer)

    def check_weekday(self):
        week_dict = {
            0: "Segunda",
            1: "Terça",
            2: "Quarta",
            3: "Quinta",
            4: "Sexta",
            5: "Sábado",
            6: "Domingo"
        }

        self.update(weekday=week_dict[self.weekday_number])

    def postfunctions(self):
        self.check_weekday()

    @property
    def senior_date(self):
        return f"{self.day}/{self.month}/{self.year}"


