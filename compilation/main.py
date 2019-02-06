#!/usr/bin/python3

import argparse
import subprocess

from compilation.environment import get_environment_details, print_environment_details
from compilation.configuration import create_configuration, print_configuration
from compilation.Logger import Logger
import compilation.settings as settings


def parser():
    parser = argparse.ArgumentParser(
        description=""  # TODO: Fill the description
    )
    parser.add_argument(
        "incremental",
        type=int,
        help="Optional. Provide the number of additional incremental "
             "compilation. Have to be 0 or over.",
        nargs='?',
        default=0
    )
    parser.add_argument(
        "-s", "--silent",
        action="store_true",
        help="Prevent printing on standard output when compiling."
    )
    parser.add_argument(
        "--tiny",
        action="store_true",
        help="Use Linux tiny configuration. Incompatible with --config "
             "argument."
    )
    parser.add_argument(
        "--config",
        help="Give a path to specific configuration file. Incompatible with "
             "--tiny argument."
    )
    return parser.parse_args()


def update_system(logger):
    logger.timed_print_output("Update of package manager (apt).")
    subprocess.run(
        "apt-get update && apt-file update",
        shell=True,
        check=True,
        stdout=logger.get_stdout_pipe(),
        stderr=logger.get_stderr_pipe()
    )


def create_logger(silent):
    return Logger(
        settings.OUTPUT_FILE,
        settings.STDOUT_FILE,
        settings.STDERR_FILE,
        silent
    )


def retrieve_and_display_environment(logger):
    logger.timed_print_output("Getting environment details.")
    environment = get_environment_details()
    print_environment_details(environment, logger.print_output)
    return environment


def retrieve_and_display_configuration(logger, args):
    logger.timed_print_output("Getting configuration details.")
    configuration = create_configuration(args)
    print_configuration(configuration, logger.print_output)
    return configuration


if __name__ == "__main__":
    args = parser()
    logger = create_logger(args.silent)
    environment = retrieve_and_display_environment(logger)
    configuration = retrieve_and_display_configuration(logger, args)

    update_system(logger)
