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
import imapclient
import joppy


def main(args):
    """ Main entry point of the app """
    logger.setLevel(args.log_level)
    logger.info("Starting Joplin Mail Gateway ....")

    # get configuration
    config = yaml.safe_load(open(args.conf_file))
    logger.info(f"Configuration read from : {args.conf_file}")
    logger.debug(f"Configuration: {config}")



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