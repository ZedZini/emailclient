import re
import smtplib
import argparse
import logging
import sqlite3
import uuid
import time
import random

import mimetypes

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders

from libs.PrettyOutput import *

global db

        else:
            return True
    elif force is True:
        output_indifferent("Forced yes")
        return True
    else:
        raise TypeError("Passed in non-boolean")


def get_interactive_email():
    email_text = ""

    # Read email text into email_text
    output_info("Enter HTML email line by line")
    output_info("Press CTRL+D to finish")
    while True:
        try:
            line = raw_input("| ")
            email_text += line + "\n"
        except EOFError:
            output_info("Email captured.")
            break

    return email_text


def get_file_email():
    email_text = ""
    try:
        with open(args.email_filename, "r") as infile:
            output_info("Reading " + args.email_filename + " as email file")
            email_text = infile.read()
    except IOError:
        output_error("Could not open file " + args.email_filename)
        exit(-1)

    return email_text


def is_domain_spoofable(from_address, to_address):
    email_re = re.compile(".*@(.*\...*)")

    from_domain = email_re.match(from_address).group(1)
    to_domain = email_re.match(to_address).group(1)
    output_info("Checking if from domain " + Style.BRIGHT + from_domain + Style.NORMAL + " is spoofable")

    if from_domain == "gmail.com":


def save_tracking_uuid(email_address, target_uuid):
    global db
    db.execute("INSERT INTO targets(email_address, uuid) VALUES (?, ?)", (email_address, target_uuid))
    db.commit()


def create_tracking_uuid(email_address):
    tracking_uuid = str(uuid.uuid4())
    save_tracking_uuid(email_address, tracking_uuid)
    return tracking_uuid


def inject_tracking_uuid(email_text, tracking_uuid):
    TRACK_PATTERN = "\[TRACK\]"

    print "Injecting tracking UUID %s" % tracking_uuid

    altered_email_text = re.sub(TRACK_PATTERN, tracking_uuid, email_text)
    return altered_email_text


def inject_name(email_text, name):
    NAME_PATTERN = "\[NAME\]"
    print "Injecting name %s" % name

    altered_email_text = re.sub(NAME_PATTERN, name, email_text)
    return altered_email_text


def delay_send():
    sleep_time = random.randint(1, 55) + (60*5)
    time.sleep(sleep_time)


if __name__ == "__main__":
    global db


        except IOError as e:
            logging.error("Could not locate file %s", args.to_address_filename)
            raise e

        for to_address in to_addresses:
            msg["To"] = to_address

            if args.track:
                tracking_uuid = create_tracking_uuid(to_address)
                altered_email_text = inject_tracking_uuid(email_text, tracking_uuid)
                msg.attach(MIMEText(altered_email_text, 'html', 'utf-8'))
            else:
                msg.attach(MIMEText(email_text, 'html', 'utf-8'))

            if args.attachment_filename is not None:
#my email address is a riddle!
                ctype, encoding = mimetypes.guess_type(args.attachment_filename)
                if ctype is None or encoding is not None:
                    # No guess could be made, or the file is encoded (compressed), so
                    # use a generic bag-of-bits type.
                    ctype = 'application/octet-stream'
                maintype, subtype = ctype.split('/', 1)
                with open(args.attachment_filename, "rb") as attachment_file:
                    inner = MIMEBase(maintype, subtype)
                    inner.set_payload(attachment_file.read())
                    encoders.encode_base64(inner)
                inner.add_header('Content-Disposition', 'attachment', filename=args.attachment_filename)
                msg.attach(inner)

            server.sendmail(args.from_address, to_address, msg.as_string())
            output_good("Email Sent to " + to_address)
            if args.slow_send:
                delay_send()
                output_info("Connecting to SMTP server at " + args.smtp_server + ":" + str(args.smtp_port))
                server = smtplib.SMTP(args.smtp_server, args.smtp_port)

    except smtplib.SMTPException as e:
        output_error("Error: Could not send email")
        raise e
