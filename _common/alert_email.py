import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(body, to_email):
	subject = "CVE DAILY ALERT: Affected you have follow create new CVE"
	# Set up the connection parameters

	smtp_server = "smtp.gmail.com"
	port = 465  # For SSL
	sender_email = "okthichiatay77@gmail.com"  # Replace with your Gmail email address
	password = "mrft caad svmc nmqb"  # Replace with your Gmail password

	# Create a MIMEText object with the email body
	message = MIMEMultipart()
	message["From"] = sender_email
	message["To"] = to_email
	message["Subject"] = subject

	# Attach the body to the email
	message.attach(MIMEText(body, "plain"))

	# Establish a secure connection with the SMTP server
	context = ssl.create_default_context()
	with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
		# Log in to your Gmail account
		server.login(sender_email, password)

		# Send the email
		server.sendmail(sender_email, to_email, message.as_string())

