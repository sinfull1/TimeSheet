import calendar
import datetime
from pprint import pprint as pp
import sys


def get_datetime_range(year, month):
    nb_days = calendar.monthrange(year, month)[1]
    datesInMonth = []
    dayOfMonth  = []
    for day in range(1, nb_days+1):
        dateObj = datetime.date(year, month, day)
        datesInMonth.append(dateObj)
        dayOfMonth.append(calendar.day_name[dateObj.weekday()])
    return (datesInMonth,dayOfMonth)


currentDate = datetime.datetime.now()
currentMonth = currentDate.month
currentYear= currentDate.year
dObj,dMon = get_datetime_range(currentYear, currentMonth)
# pp (dObj)
# pp (dMon)

# if __name__ == '__main__':
#     get_datetime_range(sys.argv[1],sys.argv[2])