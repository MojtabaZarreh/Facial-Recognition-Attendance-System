import pytz
import jdatetime
from datetime import *

def current_time(x):
    tehran_tz = pytz.timezone('Asia/Tehran')
    tehran_tz = datetime.now(tehran_tz)
    date = jdatetime.date.fromgregorian(date=tehran_tz)
    date_str = date.strftime('%Y-%m-%d')
    time = tehran_tz.strftime('%H:%M:%S')

    days_translation = {
        "Monday": "دوشـــــــنبه",
        "Tuesday": "سه‌شـــــــنبه",
        "Wednesday": "چهـــــــارشنبه",
        "Thursday": "پنـــــــج‌شنبه",
        "Friday": "جمــــــــعه",
        "Saturday": "شنــــــــبه",
        "Sunday": "یک‌شــــــــنبه"
    }
    
    english_weekday = tehran_tz.strftime('%A')
    persian_weekday = days_translation[english_weekday]    
    datetime_full = f'{date_str}-{time}'
    
    if x == 'time':
        return time
    elif x == 'date':
        return date_str
    elif x == 'weekday':
        return persian_weekday
    else:
        return datetime_full

# print(current_time('weekday'))