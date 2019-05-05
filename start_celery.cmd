@echo off
celery -A tasks worker -n emailworker --pool=solo -l info