if not DEFINED IS_MINIMIZED set IS_MINIMIZED=1 && start "" /min "%~dpnx0" %* && exit
python C:\EfcoWebClient\server_sa.py runserver -h localhost -p 80 -d
exit
