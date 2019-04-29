# -----------------------------------------------+
# EMAIL SERVICE SERVER                           +
# -----------------------------------------------+

# IMPORT ----------------------------------------+
import time
import sqlalchemy as db
from celery import Celery                           # Initialize Celery
from pytz import timezone                           # Singapore Time Format
from datetime import datetime as dt                 # Display Current time

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

# FUNCTIONS -------------------------------------+
def getData(time_data):
    query   = db.select([table]).where(db.and_(table.columns.timestamp == time_data, table.columns.status == "notsend"))
    result  = conn.execute(query).fetchall()
    return result

def updateData(eventid):
    query   = db.update(table).values(status = 'send').where(table.columns.event_id == eventid)
    result  = conn.execute(query)

# RUN -------------------------------------------+
if __name__ == "__main__":
    print("Email Server is running!")
    while True:
        mytime = dt.now().strftime("%d %b %Y %H:%M")
        result = getData(mytime)
        for data in result:
            sendMail.delay(data.event_id)
            time.sleep(10)
        time.sleep(10)
# END -------------------------------------------+


