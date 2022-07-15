from datetime import date, timedelta


def time_window(start_date, end_date):

    from_year, from_month, from_day = start_date.split("-")
    to_year, to_month, to_day = end_date.split("-")

    start_date = date(int(from_year), int(from_month), int(from_day))
    end_date = date(int(to_year), int(to_month), int(to_day))

    actual_date = start_date

    all_dates = [start_date, end_date]
    while actual_date < end_date:
        new_date = actual_date + timedelta(days=1)
        all_dates.append(new_date)
        actual_date = new_date

    all_dates = list(set(all_dates))
    print("Dates to be analised:", all_dates)
    return all_dates
