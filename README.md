# pyPing

Tool to log pings with datetime values

prequesits:
- pythonping (pip pythonping)

parameters:

- -t --target (default localhost);   host you want to ping 
-  -to --timeout (default 1);           time in secondes to wait between pings
  - -lf --logfile
  - -ll --loglevel (default INFO); chaise between 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'
  - -tp --template (default internet); choices between 'lan', 'internet'

example:

pyPing.py --target www.google.com --logfile /var/log/ping.log --loglevel WARNING

