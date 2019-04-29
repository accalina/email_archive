@echo off
celery -A tasks worker --pool=solo -l info