import os.path
import shlex
import subprocess
from engineio.async_drivers import gevent
import pywintypes
import win32api
import cffi
import sys
import logging
import threading
# import xlsxwriter
from datetime import datetime
from gensim.models.keyedvectors import KeyedVectors
from datetime import date
import easygui
import joblib
import pandas as pd
import requests
# from reportlab.pdfgen import canvas
from slackclient import SlackClient
from slackeventsapi import SlackEventAdapter
from expiry_testing import program_expired
import os
from DocSim import DocSim
from Clean import Clean
# from reporting import generateReport
# from flask_cors import CORS
# from overall_report import date_filter, UWQS, QSR, QSRlog, upload_report
# from overall_report import complete_report, upload_report
from flask import Flask
from charts import report_fromslack_to_html
from flask import Flask, render_template, jsonify, url_for
from flask_socketio import SocketIO, send, emit
import logging.handlers

LOG_FILENAME='demo.out'
log=logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

logger=logging.getLogger("slackapp")
logger.setLevel(logging.DEBUG)

# # create file handler which logs even debug messages
# fh = logging.FileHandler("demo.log")
# fh.setLevel(logging.DEBUG)


# Add the log message handler to the logger
fh=logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=1024*1024*50, backupCount=10)
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch=logging.StreamHandler()
ch.setLevel(logging.ERROR)

# create formatter and add it to the handlers
formatter=logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt='%m/%d/%Y %I:%M:%S %p')
ch.setFormatter(formatter)
fh.setFormatter(formatter)

# add the handlers to logger
logger.addHandler(ch)
logger.addHandler(fh)

# 'application' code
# "application" code
# logger.debug("debug message")
# logger.info("info message")
# logger.warn("warn message")
# logger.error("error message")
# logger.critical("critical message")

real_name='rahul'
event_ts='1587220074.002500'
TSS='17-04-2020'
TSE='17-04-2020'
separator="="
keys={}
with open('property.config') as f:
    for line in f:
        if separator in line:
            # Find the name and value by splitting the string
            name, value=line.split(separator, 1)
            # Assign key value pair to dict
            # strip() removes white space from the ends of strings
            keys[name.strip()]=value.strip()
# print(keys)

# print(keys['slack_signing_secret'])
app=Flask(__name__, static_folder='static', template_folder='templates')
app.config['SECRET_KEY']='replace later'

# Our app's Slack Event Adapter for receiving actions via the Events API
slack_signing_secret=keys['slack_signing_secret']
# print(slack_signing_secret)
slack_events_adapter=SlackEventAdapter(slack_signing_secret, keys['slack_events_adapter_url_extension'], app)
# print(keys['slack_events_adapter_url_extension'])
# Create a SlackClient for your bot to use for Web API requests
slack_bot_token=keys['slack_bot_token']
slack_client=SlackClient(slack_bot_token)
ds=joblib.load('./data/model.pkl')

# #################
p=Clean('./data/Complete_clean_data_with_product_information.csv')
dataframe=p.dataframe('./data/Complete_clean_data_with_product_information.csv')


#
# all_user_search = []
# username ="sam"
@slack_events_adapter.on("message")
def handle_message(event_data):
    message = event_data["event"]
    x = threading.Thread(
                target=main_def,
                args=(message,)
    )
    x.start()
    
def main_def(message,):
    global event_ts
    global real_name
    username = message.get('text')
    event_ts = message.get('event_ts')
    user = message.get('user')
    sam = slack_client.api_call('users.info', user=user)
    real_name = sam['user'].get('real_name')
    channel = message["channel"]
    print("channel source:", channel)

    if channel == keys['channel']:
        if real_name == keys['app_name']:
            print("app cannot send the data to input channel")
        else:
            x = threading.Thread(
                target=some_processing,
                args=(username, event_ts, real_name,)
            )
            x.start()

    elif channel == keys['channel_report']:
        if real_name == keys['app_name']:
            print("app cannot send the data to report channel")
            # sys.exit()
        elif '@report' in username:
            x = threading.Thread(
                target=todays_report,
                args=(event_ts, keys, real_name,)
            )
            x.start()
        else:
            slack_client.api_call("chat.postMessage", channel=keys['channel_report'],
                                  text='This message is not supported in this channel, it should be used only for generating report.')
            logger.warning(
                'This message is outside the scope of this Channel!. Please contact the system administrator of this application')  # will print a message to the console
    else:
        print("not a valid channel")


def todays_report(event_ts, keys, real_name, ):
    global TSS
    if real_name == keys['app_name']:
        print("app cannot send the data to input channel")
    else:
        program_expired(event_ts)
        timestamp=int(float(event_ts))
        dt_object=datetime.fromtimestamp(timestamp)
        sam=str(dt_object).split()[0]
        sam=sam.split('-')
        sam=sam[::-1]
        sam='-'.join(sam)
        TSE=sam
        slack_client.api_call("chat.postMessage", channel=keys['channel_report'],
                              text='please connect to link %s/%s'%(keys['MachineName'], real_name))
        logger.info(timestamp)
        print("report sent")
        logger.info("Generating charts")
    return report_fromslack_to_html(TSS, TSE)


def some_processing(username, event_ts, real_name, ):
    if real_name == keys['app_name']:
        print("app cannot send the data to input channel")
    else:
        program_expired(event_ts)
        timestamp=int(float(event_ts))
        dt_object=datetime.fromtimestamp(timestamp)
        d1=str(dt_object).split()[0]
        d1=d1.split('-')
        d1=d1[::-1]
        d1='-'.join(d1)
        logger.info("step1")
        user_name=real_name
        source_doc=username
        target_docs=p.cleaning('./data/Complete_clean_data_with_product_information.csv')
        splitting=source_doc.split()
        if len(splitting) > 3:
            try:
                sim_scores=ds.calculate_similarity(source_doc, target_docs)
                index=sim_scores[0]['index']
                print(sim_scores[0])
                logger.info(timestamp, sim_scores[0])
                output=dataframe.iloc[index, 2]
            except IndexError as error:
                output="No Category"
        else:
            output="No Category"
        df = pd.read_csv("./data/result.csv", index_col="Unnamed: 0")
        df.drop_duplicates(keep='first', inplace=True)
        df2 = pd.DataFrame({'time': [d1], 'user_name': [user_name], 'User_query': [username], 'Category': [output]})
        df3 = df2.append(df)
        df3.to_csv("./data/result.csv")
        print('stored in database')


socketio=SocketIO(app)


@app.route('/', methods=['GET', 'POST'])
@app.route('/<name>')
def index(name=None):
    logger.info(real_name)
    return render_template('chart.html', name=name)


@socketio.on('message')
def message(data):
    # print(f"/n/n{data}/n/n")
    logger.info("viewed")
    data=report_fromslack_to_html(TSS, TSE)
    # data = tc_report(TSS, TSE, keys)
    # print("data that needs to be sent", data)
    # print("event_ts value is", event_ts)
    send(data, broadcast=True)


# Once we have our event listeners configured, we can start the
# Flask server with the default `/events` endpoint on port 3000
# slack_events_adapter.start(port=keys['port_number'])
if __name__ == "__main__":
    # app.run(port=5000, debug=True)
    socketio.run(app, debug=True, port=5000)
