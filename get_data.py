import csv
import time
import datetime
import smtplib
import settings

def csv_data():
	with open('/home/pi/speed_data.csv', 'r') as f:
		reader = csv.reader(f)
		data = list(reader)

		# to get today's average, start counting from the last rows
		last_row = len(data)-1

		ts = time.time()
		date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
		
		down_avg = 0
		up_avg = 0
		ping_avg = 0
		day_count = 0

		for i in range(last_row, 0, -1):
			time_check = data[i][0].split(' ')
			if time_check[0] == date:
				down_avg += float(data[i][1])
				up_avg += float(data[i][2])
				ping_avg += float(data[i][3])
				day_count += 1
			else:
				break

		down_avg = round((down_avg/day_count), 3)
		up_avg = round((up_avg/day_count), 3)
		ping_avg = round((ping_avg / day_count), 3)

	return [date, down_avg, up_avg, ping_avg]

def contact(results):
	gmail_smtp = 'smtp.gmail.com'
	port = 587

	server = smtplib.SMTP(gmail_smtp, port)
	server.ehlo()
	server.starttls()
	server.login(settings.email_account, settings.email_pw)

	msg = '''Subject: Network summary for {}\nAverage download speed = {} Mbps\nAverage upload speed = {} Mbps\nAverage ping = {} ms'''.format(results[0], results[1], results[2], results[3])

	server.sendmail(settings.email_account, settings.email_to, msg)
	server.quit()

if __name__ == '__main__':
	results = csv_data()
	contact(results)