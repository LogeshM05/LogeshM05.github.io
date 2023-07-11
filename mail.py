# from flask import Flask, request

# app = Flask(__name__)

# @app.route("/start")
def showHomePage():
      # response from the server
    return "This is home page"

# @app.route("/email_push", methods=["POST"])
def email_push():
    email = request.form["email"]
    subject = request.form["subject"]
    body = request.form["body"]

    # Perform email push logic here using a library or API of your choice
    # For example, using the smtplib library
    import smtplib
    from email.mime.text import MIMEText

    # Set up email details
    sender_email = "logeshwarsathya@gmail.com"
    recipient_email = email
    email_subject = subject
    email_body = body

    msg = MIMEText(email_body)
    msg["Subject"] = email_subject
    msg["From"] = sender_email
    msg["To"] = recipient_email

    print(email_subject)
    print(email_body)
    print(recipient_email)



    # Send email
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login("logeshwarsathya@gmail.com", "apzbrflcezulsnoz")
            server.sendmail(sender_email, recipient_email, msg.as_string())
    except Exception as e:
        print("Error sending email:", str(e))
        return "Error sending email"
    
    return "sent"

if __name__ == "__main__":
  app.run(host="0.0.0.0")
