import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(sender_email, receiver_email, subject, message):
    # Email configuration
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'logeshwarsathya@gmail.com'
    smtp_password = 'apzbrflcezulsnoz'

    # Create a multipart email message
    email_message = MIMEMultipart()
    email_message['From'] = sender_email
    email_message['To'] = receiver_email
    email_message['Subject'] = subject

    # Add the message to the email
    email_message.attach(MIMEText(message, 'plain'))
    print(sender_email)
    print(receiver_email)
    print(subject)
    print(message)

    # Send the email
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(email_message)
        return 'Email sent successfully'
    except smtplib.SMTPException as e:
        return 'Error sending email: ' + str(e)

