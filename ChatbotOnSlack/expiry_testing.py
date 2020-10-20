from datetime import datetime
import easygui
import logging

module_logger = logging.getLogger('slackapp.tes')

def program_expired(event_timestamp):
    dt_object = datetime.fromtimestamp(int(float(event_timestamp)))
    covert_date = str(dt_object).split()[0]
    event_year = int(covert_date.split()[0].split('-')[0])
    event_month = int(covert_date.split()[0].split('-')[1])
    event_day = int(covert_date.split()[0].split('-')[2])
    slack_date = datetime(year=event_year, month=event_month, day=event_day)  # setup a datetime object
    read_input = '2020-05-03'
    year = int(read_input.split()[0].split('-')[0])
    month = int(read_input.split()[0].split('-')[1])
    day = int(read_input.split()[0].split('-')[2])
    app_date = datetime(year=year, month=month, day=day)  # setup a datetime object
    totalDays = (slack_date) - (app_date)
    module_logger.info(totalDays.days)
    if 80 < totalDays.days < 90:  # change to 30
        easygui.msgbox(('Your trial period is about to be over in ' + str(90 - totalDays.days) + ' days'),
                       title="Alert Message")
    elif totalDays.days > 90:
        easygui.msgbox(('Your trial period is about to be over please get the updated version'),
                       title="Alert Message")
        exit()