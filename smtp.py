import os
import sys
import logging
import smtplib
import socket
from email.message import EmailMessage


class SmtpApi(object):
    """
    Wrapper around SMTP. Used to send email
    """
    def __init__(self, log, smtp_address, from_email, port,
                 username=None, password=None):
        self.port = port
        self.log = log
        self.smtp_address = smtp_address
        self.from_email = from_email
        self.username = username
        self.password = password

    def send_email(self, to_email_address, subj=None, msg=None):
        error = None
        validation_error = False
        if msg is None:
            msg  = "TEST_EMAIL_MESSAGE"
        if subj is None:
            subj  = "TEST_EMAIL_SUBJECT"
        try:
            email = EmailMessage()
            email.set_content(msg)
            email['Subject'] = subj
            email['From'] = self.from_email
            email['To'] = to_email_address
            # Timeout on rest apis is 30 secs so need
            # a timeout less than this
            self.log.info("SMTP Connecting...")
            smtp = smtplib.SMTP(self.smtp_address, timeout=25,
                                port=self.port)
            self.log.info("SMTP Connected")
            smtp.ehlo()
            smtp.starttls()
            if self.username is not None and self.password is not None:
                smtp.login(self.username, self.password)
                self.log.info("SMTP Logged in")
            smtp.send_message(email)
            self.log.info("SMTP Sent email successfully.")
            smtp.quit()

        except smtplib.SMTPServerDisconnected:
            error = "SMTP_SERVER_DISCONNECTED"
        except smtplib.SMTPSenderRefused:
            validation_error = False
            error = "SMTP_SENDER_REFUSED"
        except smtplib.SMTPRecipientsRefused:
            validation_error = False
            error = "SMTP_RECIPIENT_REFUSED"
        except smtplib.SMTPDataError:
            error = "SMTP_DATA_ERROR"
        except smtplib.SMTPConnectError:
            error = "SMTP_CONNECTION_ERROR"
        except smtplib.SMTPHeloError:
            error = "SMTP_HELO_ERROR"
        except smtplib.SMTPNotSupportedError:
            error = "SMTP_NOT_SUPPORTED_ERROR"
        except smtplib.SMTPAuthenticationError:
            validation_error = False
            error = "SMTP_AUTH_ERROR"
        except smtplib.SMTPResponseException:
            error = "SMTP_RESPONSE_EXCEPTION"
        except smtplib.SMTPException:
            error = "SMTP_GENERAL_ERROR"
        except socket.error:
            # Get this error if port is wrong or ip wrong
            error = "SMTP_SOCKET_CONNECTION_ERROR"
        except Exception:
            self.log.exception("General Error sending email address")
            raise
        if error is not None:
            self.log.error("SMTP error code '%s'", error)



logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("./test_smtp.log"),
        logging.StreamHandler()
    ]
)

SETTINGS = ["SMTP_DOMAIN_NAME", "SMTP_USER", "SMTP_PASS", "SMTP_FROM_EMAIL_IN_ORG",
            "SMTP_TO_EMAIL_IN_ORG", "SMTP_TO_EMAIL_OUTSIDE_ORG"]

def getSettings():
    config = {}
    for setting in SETTINGS:
        value = os.getenv(setting)
        if value is None:
            print("Required Env variable '%s' is missing." %setting)
            print("Must set all of the following env variables to proceed:")
            print(str(SETTINGS))
            sys.exit(-1)
        else:
            config[setting] = value
    return config


settings = getSettings()
# These case work because we have logged in so he can use server as a relay to send
# message outside of org. If we don't login then can only send email to somebody at
# zippy.zapto.org
api = SmtpApi(logging, settings["SMTP_DOMAIN_NAME"], settings["SMTP_FROM_EMAIL_IN_ORG"],
               25, settings["SMTP_USER"], settings["SMTP_PASS"])
api.send_email(settings["SMTP_TO_EMAIL_OUTSIDE_ORG"])
api = SmtpApi(logging, settings["SMTP_DOMAIN_NAME"], settings["SMTP_FROM_EMAIL_IN_ORG"], 25)
api.send_email(settings["SMTP_TO_EMAIL_IN_ORG"])

