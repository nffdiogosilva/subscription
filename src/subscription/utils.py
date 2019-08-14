import datetime

def get_year_total_days(year=None):
    """Util function that calculates the total days a year have."""

    # gets current year if no year has been passed as argument
    year = year or datetime.datetime.now().year

    first_day_year = datetime.date(year, 1, 1)
    last_day_year = datetime.date(year, 12, 31)

    # needs to add one more day so we get 365/366 results
    return (last_day_year - first_day_year).days + 1
 