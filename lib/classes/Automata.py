import datetime
import time
import webbrowser

import pyautogui
import pyperclip

from lib.functions.get_config import get_config
from lib.models.CalendarEvent import CalendarEvent
from lib.models.EventAlias import EventAlias
from lib.models.SeniorRegister import SeniorRegister


class Automata:

    def hotkey(self, k1, k2):
        pyautogui.hotkey(k1, k2)
        return self

    def copy_clipboard(self):
        pyautogui.hotkey('command', 'c')
        time.sleep(.01)  # ctrl-c is usually very fast but your program may execute faster
        return pyperclip.paste()

    def __init__(self):
        self.screen_width, self.screen_height = pyautogui.size()

    def drag_to(self, x, y):
        pyautogui.dragTo(x, y, button='left')
        return self

    def get_mouse_pos(self):
        return pyautogui.position()

    def move_mouse_to(self, x, y, duration=0.0):
        pyautogui.moveTo(x, y, duration=duration, tween=pyautogui.easeInOutQuad)
        return self

    def click(self, what=""):
        if what != "":
            pyautogui.click(what)
        else:
            pyautogui.click()
        return self

    def write(self, text, interval=0):
        pyautogui.write(text, interval=interval)
        return self

    def press(self, key):
        pyautogui.press(key)
        return self

    def alert(self, message):
        pyautogui.alert(message)
        return self

    def discover_mouse_pos(self):
        while True:
            time.sleep(1)
            print(self.get_mouse_pos())

    def infinite_clicking(self, position):
        x, y = position
        self.move_mouse_to(x, y, duration=1)
        while True:
            self.click()

    def find_and_click(self, text):
        pyautogui.hotkey("command", "f")
        self.write(text)
        pyautogui.hotkey('ctrlleft', 'enter')
        return self

    def select_and_save(self, from_coords, to_coords, mode=str):
        from_x, from_y = from_coords
        to_x, to_y = to_coords
        self.move_mouse_to(from_x, from_y)
        pyautogui.dragTo(to_x, to_y, button="left")
        return mode(self.copy_clipboard())

    def get_value(self):
        return str(self.copy_clipboard())

    @property
    def calendar(self):
        return self.Calendar(self)

    class Calendar:

        def __init__(self, auto):
            self.automata = auto

        def issue_summary(self):
            self.automata.press("tab")
            issuekey, summary = self.automata.copy_clipboard().split(" | ")
            self.automata.hotkey()
            return issuekey, summary

        def get_events_for_day(self, target_date):

            cfg = get_config()
            events = []

            # Config
            nonbillableterms = cfg['calendar']['non_billable']
            summary = ""
            issuekey = ""
            description = ""

            # Declare Automator
            auto = Automata()

            # Open Chrome
            chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
            url = f"https://calendar.google.com/calendar/u/0/r/day/{target_date.year}/{target_date.month}/{target_date.day}"
            webbrowser.get(chrome_path).open(url)

            # Wait x seconds
            time.sleep(4)

            pyautogui.hotkey("command", "f", interval=0.20)
            pyautogui.write(cfg['senior']['start_time_placeholder'], interval=0.05)
            pyautogui.hotkey("ctrl", "enter", interval=0.20)

            # Edit first
            is_running = True

            # Create placeholder for Senior Registers
            senior_log_data = SeniorRegister(day=target_date.day, month=target_date.month, year=target_date.year, weekday_number=target_date.weekday())

            while is_running:

                # By standard, all logs should be billable, but some are internal or nb
                billable = False
                is_referential = False
                ignore_event = False
                reference_type = ""

                pyautogui.press("e")
                time.sleep(3)
                pyautogui.press("tab")
                summary = auto.get_value().replace("❇️", "").strip()

                for eti in cfg["calendar"]["events_to_ignore"]:
                    if eti in summary:
                        ignore_event = True

                try:
                    billable = True
                    issuekey, description = summary.split(f"{cfg['calendar']['issue_key_separator']}")

                    # Treat data briefly
                    description = description.strip()
                    issuekey = issuekey.strip()

                except:
                    issuekey = "No Issue"
                    description = summary

                for string_match in cfg["calendar"]["internal_hour_events"]:
                    if string_match in summary:
                        issuekey = cfg["calendar"]["internal_meetings_issue"]

                aliases = EventAlias.query.all()
                for alias in aliases:
                    if str(alias.match).lower() in summary.lower():
                        issuekey = alias.issue_key

                pyautogui.press("tab")
                pyautogui.press("tab")
                pyautogui.press("tab")
                google_date = auto.get_value()
                pyautogui.press("tab")
                start_time = auto.get_value()
                pyautogui.press("tab")
                end_time = auto.get_value()
                pyautogui.press("esc")
                time.sleep(1)
                pyautogui.press("tab")
                pyautogui.press("enter")

                for event_name in [cfg["senior"]['start_time_placeholder'],
                                   cfg["senior"]['lunch_time_placeholder'],
                                   cfg["senior"]['end_time_placeholder']]:

                    if summary == event_name:
                        is_referential = True
                        reference_type = event_name

                if summary == cfg["senior"]['start_time_placeholder']:
                    senior_log_data.update(entry_1=end_time)

                elif summary == cfg["senior"]['lunch_time_placeholder']:
                    senior_log_data.update(leave_1=start_time, entry_2=end_time)

                elif summary == cfg["senior"]['end_time_placeholder']:
                    senior_log_data.update(leave_2=start_time)


                tempo_datetime = f"{target_date.year}-{target_date.month}-{target_date.day}T{start_time}:00.000"

                # Register the event from calendar to the database
                if not ignore_event:
                    events.append(CalendarEvent(
                        original_summary=summary,
                        issue_key=issuekey,
                        event_date=datetime.date(target_date.year, target_date.month, target_date.day),
                        description=description,
                        start_time=start_time,
                        billable=billable,
                        end_time=end_time,
                        original_tempo_datetime=tempo_datetime,
                        is_referential=is_referential,
                        reference_type=reference_type,
                        is_logged=1 if is_referential else 0,
                        google_date=google_date,
                        year=target_date.year,
                        month=target_date.month,
                        day=target_date.day
                    ))

                    if summary == cfg['senior']['last_event_of_the_day']:
                        is_running = False

            # Close
            pyautogui.press("esc", presses=3, interval=0.20)
            pyautogui.hotkey("command", "w", interval=0.20)
