

from datetime import datetime, timedelta
from pytz import timezone
from celery import Celery

app = Celery('wip_task', broker="amqp://localhost//")  # Connect Celery to RabitMQ Server

@app.task
def test(username):
    print("hello {}".format(username))


if __name__ == "__main__": 
    # [*] Get Timezone from Time
    # mytime = "01 May 2019 20:57 +0700"
    # timedc = datetime.strptime(mytime, "%d %b %Y %H:%M %z")
    # print(timedc.tzname())

    # [*] Get Timezone from Encoding and Decoding with stt
    # mytime = datetime.now(tz=timezone('Asia/Jakarta'))
    # timeec = datetime.strftime(mytime, "%d %b %Y %H:%M %z")
    # print(timeec)
    # timedc = datetime.strptime(timeec, "%d %b %Y %H:%M %z")
    # print(timedc)
    # print(timedc.tzname())

    # [*] Applying Timezone to Task with ETA
    mytime = "01 May 2019 20:52 +0700"
    now = datetime.strptime(mytime, "%d %b %Y %H:%M %z")
    target = now + timedelta(seconds=10)
    print(target)
    test.apply_async(args=["accalina"],eta=target)
