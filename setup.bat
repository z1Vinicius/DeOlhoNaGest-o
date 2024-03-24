@echo off
:loop
echo Re-starting Django Server
py manage.py runserver 192.168.18.3:8000
ping 127.0.0.1 -n 5 > nul
goto loop