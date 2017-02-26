import os
import sys
import csv
import datetime
import time
import re
import settings
import tweepy

def speed_test():
    ts = time.time()

    # use HTTPS to communicate with speedtest servers
    test = os.popen('/usr/local/bin/speedtest-cli --secure').read()

    # if speedtest could not connect set the speeds to 0
    if 'Cannot' in test:
        outage = True 
        ping = 1000
        download = 0
        upload = 0

    # extract data from results displayed by program
    else:
        outage = False
        regex = r'\d?\d?\d[.]\d\d?\d?'
        speeds = re.compile(regex)
        speeds = speeds.findall(test)
        ping = float(speeds[3])
        download = float(speeds[4])
        upload = float(speeds[5])

    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    results = [date, download, upload, ping]

    with open('/home/pi/speed_data.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(results)
  
   # connect to twitter
   auth = tweepy.OAuthHandler(settings.con_key, settings.con_secret)
   auth.set_access_token(settings.a_tok, settings.a_secret)

   api = tweepy.API(auth)

   # try to tweet if speedtest couldnt even connect
   if outage is True:
       try:
           tweet = 'Hey @Comcast @ComcastCares why is my internet down? I pay for 150down//10up in Washington, DC. #comcastoutage #comcast'
           api.update_status(tweet)
       except:
           pass

   # tweet if down speed is less than whatever I set
   elif download < 100:
       try:
           tweet = 'Hey @Comcast why is my internet speed {}down//{}up when I pay for 150down//10up in Washington, DC? @ComcastCares @xfinity #comcast'.format(download, upload)
           
           api.update_status(tweet)

       except Exception as e:
           print(str(e))

if __name__ == '__main__':
    speed_test()
