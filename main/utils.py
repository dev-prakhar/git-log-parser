import subprocess

from constants import GIT_VALID_DIRECTORY_COMMAND, GIT_LOG_COMMAND, NON_ZERO_CODE_ERROR, COMMIT
from exceptions import NonZeroExitCodeException


def execute_command(command):
    """
    Method to execute command in shell
    :param command:
    """
    exit_code = subprocess.call(command, shell=True)
    if exit_code:
        raise NonZeroExitCodeException(NON_ZERO_CODE_ERROR)
    return exit_code

def get_output(command):
    """
    Method to execute command in shell and get the output of the command in string format
    :param command:
    :return: string output of the executed command
    """
    return subprocess.check_output(command, shell=True).decode('utf-8')

def get_cleaned_log(raw_log):
    """
    Method to clean the log from stray spaces and new lines
    :param raw_log:
    :return: list of string without stray spaces and new lines
    """
    return [line.strip() for line in raw_log if line]

def get_git_log_contents(directory, log_count):
    """
    Method to get git log contents for the given directory and log count
    :param directory
    :param log_count:
    :return: list of git log lines
    """
    execute_command(GIT_VALID_DIRECTORY_COMMAND.format(dir=directory))  # exception if directory is not git initialised
    git_log = get_output(GIT_LOG_COMMAND.format(dir=directory, number=log_count)).splitlines(keepends=True)

    git_logs = []
    single_log = ''
    for log in git_log:
        if log.startswith(COMMIT):
            if single_log:
                git_logs.append(single_log)
                single_log = ''
        single_log += log

    if single_log:
        git_logs.append(single_log)

    return git_logs

def get_string_after_n_space(text, n):
    """
    Method to return string after the nth space

    Input --> 'test1 test2 test3', 1
    Output --> test2 test3

    Input --> 'test1 test2 test3, 2
    Output --> test3
    :param text
    :param n:
    :return: string after nth space
    """
    return text.split(' ', n)[-1].strip()
