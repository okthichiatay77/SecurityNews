import smtplib


def send_email(to_email, title):
	server = smtplib.SMTP("smtp.gmail.com", 587)
	server.starttls()
	server.login("okthichiatay77@gmail.com", "mrft caad svmc nmqb")

	from_email = "okthichiatay77@gmail.com"
	subject = "CVE'S DAILY ALERT: Affected you have follow create new CVE"
	body = "CVE'S DAILY ALERT: Affected you have follow create new CVE, name: {}".format(title)

	server.sendmail(from_email, to_email, subject + "\n" + body)

	server.quit()

