# -----------------------------------------------+
# EMAIL SERVICE SERVER                           +
# -----------------------------------------------+

# IMPORT ----------------------------------------+
import time
import sqlalchemy as db
from celery import Celery                           # Initialize Celery
from pytz import timezone                           # Singapore Time Format
from datetime import datetime as dt, timedelta                 # Display Current time

# INIT ------------------------------------------+
app         = Celery('tasks', broker="amqp://localhost//")  # Connect Celery to RabitMQ Server
engine      = db.create_engine('sqlite:///email_database.db')
conn        = engine.connect()
metadata    = db.MetaData()
table       = db.Table('client_email', metadata, autoload=True, autoload_with=engine)

# TASKS -----------------------------------------+
@app.task
def sendMail(event_id):
    updateData(event_id)
    print("Email has been sent to EventID {}".format(event_id))

@app.task
def sendMailETA(event_id):
    engine      = db.create_engine('sqlite:///email_database.db')
    conn        = engine.connect()
    metadata    = db.MetaData()
    table       = db.Table('client_email', metadata, autoload=True, autoload_with=engine)
    query       = db.update(table).values(status = 'send').where(table.columns.event_id == event_id)
    result      = conn.execute(query)

# FUNCTIONS -------------------------------------+
def getData(time_data):
    query   = db.select([table]).where(db.and_(table.columns.timestamp == time_data, table.columns.status == "notsend"))
    result  = conn.execute(query).fetchall()
    return result

def getDataNotsend():
    query   = db.select([table]).where(table.columns.status == "notsend")
    result  = conn.execute(query).fetchall()
    return result

def updateData(eventid):
    query   = db.update(table).values(status = 'send').where(table.columns.event_id == eventid)
    result  = conn.execute(query)

# RUN -------------------------------------------+
if __name__ == "__main__":
    print("Email Server is running!")

    for item in getDataNotsend():
        # timedc = dt.strptime(item.timestamp+" +0700", "%d %b %Y %H:%M %z")
        # sendMail.apply_async(args=[item.event_id], eta=timedc)

        mytime = dt.now(tz=timezone('Asia/Jakarta'))
        target = mytime + timedelta(seconds=1)
        print(target)
        sendMailETA.apply_async(args=[5], eta=target)

    # while True:
    #     mytime = dt.now().strftime("%d %b %Y %H:%M")
    #     result = getData(mytime)
    #     for data in result:
    #         sendMail.delay(data.event_id)
    #         time.sleep(10)
    #     time.sleep(10)
# END -------------------------------------------+


