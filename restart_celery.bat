@echo off
call activate yolov8
taskkill /F /IM "celery.exe" > NUL
start /min celery -A ticker_new worker --pool=eventlet --loglevel=info
start /min celery -A ticker_new beat --loglevel=info