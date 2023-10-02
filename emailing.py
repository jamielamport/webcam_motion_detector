import smtplib
import imghdr
from email.message import EmailMessage

email_password = 'ujor hcid qics eenv'
email_user = "jamie.lamport@gmail.com"
email_recipient = "jamie.lamport@gmail.com"

def sendEmail(emailImage):
    print("Email send function started")
    email_message = EmailMessage()
    email_message["Subject"] = "A new anomoly has been detected by your webcam"
    email_message.set_content("Something has been detected by your webcam, take a look")

    with open(emailImage, "rb") as file:
        content = file.read()
    email_message.add_attachment(content, maintype="image", subtype=imghdr.what(None, content))

    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(email_user, email_password)
    gmail.sendmail(email_user, email_recipient, email_message.as_string())
    gmail.quit()
    print("Email send function ended")

if __name__ == "__main__":
    sendEmail(emailImage="images/1.png")