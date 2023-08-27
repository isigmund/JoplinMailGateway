#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Ingo Sigmund"
__version__ = "0.1.0"
__license__ = "MIT"

import argparse
from logzero import logger, logging
import yaml
from imapclient import IMAPClient
import joppy
import email
import time


def fetch_new_emails(config):
    with IMAPClient(config['imap']['server']) as server:
        server.login(config['imap']['user'], config['imap']['password'])
        server.select_folder("INBOX")

        messages = server.search("UNSEEN")
        logger.info(messages)

        for uid, message_data in server.fetch(messages, "RFC822").items():
            email_message = email.message_from_bytes(message_data[b"RFC822"])
            print(uid, email_message.get("From"), email_message.get("Subject"), email_message.get("Body"))
            email_message.get()
        
        server.logout()




def main(args):
    """ Main entry point of the app """
    logger.setLevel(args.log_level)
    logger.info("Starting Joplin Mail Gateway ....")

    # get configuration
    config = yaml.safe_load(open(args.conf_file))
    logger.info(f"Configuration read from : {args.conf_file}")
    logger.debug(f"Configuration: {config}")
    logger.debug(f"Configuration: {config['imap']['user']}")

    while True:
        try:
            fetch_new_emails(config)
            time.sleep(30)
            # TODO: every 10 minutes reestablish idle mode (server.IDLE)

        except KeyboardInterrupt:
            break







if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    # Optional argument to define location of configuration file
    parser.add_argument("-c", "--conf", action="store", dest="conf_file", default="./JoplinMailGateway.yaml")
    parser.add_argument("-l", "--loglevel", action="store", dest="log_level", default="INFO")

    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))

    args = parser.parse_args()
    main(args)