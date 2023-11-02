# refs:
# https://coderzcolumn.com/tutorials/python/smtplib-simple-guide-to-sending-mails-using-python#:~:text=Sendmail(from_addr%2C%20to_addrs%2C%20msg)%20-%20This,string%20representing%20the%20email%20address
#
# https://stackoverflow.com/questions/6270782/how-to-send-an-email-with-python
import smtplib
import time

from email.header import Header
from email.mime.text import MIMEText
from myapp.variables import *
from myapp.utils import logger

logger = logger()

def send_email( subject ="Default Subject", message = "Default_message"):
    start = time.time()
    logger.info("sending mail")
    try:
        smtp_serv = smtplib.SMTP(host=f'smtp.{SMTP_HOST}', port=SMTP_PORT)
        smtp_serv.starttls()
    except Exception as e:
        print("ErrorType : {}, Error : {}".format(type(e).__name__, e))
        smtp_serv = None
    
    if EMAIL_DEBUGGER:
        print("Connection Object : {}".format(smtp_serv))
        print("Total Time Taken  : {:,.2f} Seconds".format(time.time() - start))
    
    ######### Log In to mail account ############################
    if EMAIL_DEBUGGER:
        print("\nLogging In.....")
    resp_code, response = smtp_serv.login(user=SMTP_LOGIN, password=SMTP_PASSWORD)
    
    if EMAIL_DEBUGGER:
        print("Response Code : {}".format(resp_code))
        print("Response      : {}".format(response.decode()))
    
    # message = email.message.EmailMessage()
    # message.set_default_type("text/plain")
    message = MIMEText(message, 'plain', 'utf-8')
    message['From'] = EMAIL_FROM_NAME
    message['To'] = EMAIL_TO
    message['Subject'] = Header(subject, 'utf-8')
    
    smtp_serv.sendmail(EMAIL_FROM, EMAIL_TO, message.as_string())
    # print('mail was sent')
    logger.info("mail has been sent")
    ######### Log out to mail account ############################
    if EMAIL_DEBUGGER:
        print("\nLogging Out....")
    resp_code, response = smtp_serv.quit()
    if EMAIL_DEBUGGER:
        print("Response Code : {}".format(resp_code))
        print("Response      : {}".format(response.decode()))


if __name__ == "__main__":
    send_email(subject="Default Subject", message="Default_text")