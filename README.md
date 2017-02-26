# speedtest  

This program runs speedtest-cli every minute from a Raspberry Pi cronjob, and:  
* Writes the results to a csv file  
* Tweets Comcast/your ISP when your speeds are less than satisfactory
* Emails you a daily average of download, upload, and ping speeds

# Speedtest-cli Installation:

https://github.com/sivel/speedtest-cli

## Cron Instructions

\* * * * * /usr/bin/python3 /home/pi/speed_test.py  
59 23 * * * /usr/bin/python3 /home/pi/get_data.py
