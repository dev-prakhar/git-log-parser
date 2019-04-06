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
    return [line.strip() for line in raw_log if line.strip()]

def git_log_via_command(directory, log_count):
    """
    Method to get git log contents for the given directory and log count via git log command
    :param directory
    :param log_count:
    :return: list of git log lines
    """
    execute_command(GIT_VALID_DIRECTORY_COMMAND.format(dir=directory))  # exception if directory is not git initialised
    git_log = get_output(GIT_LOG_COMMAND.format(dir=directory, number=log_count)).splitlines(keepends=True)
    return create_git_log_content(git_log)

def git_log_via_file(file_path):
    """
    Method to get git log contents for the given directory and log count via file path
    :param file_path
    :return: list of git log lines
    """
    git_log_file = open(file_path, "r")
    git_log = git_log_file.read().splitlines(keepends=True)
    return create_git_log_content(git_log)

def create_git_log_content(git_log):
    """
    Method to generate git log list having each commit as a list item
    :param git_log:
    :return: list of git commits
    """
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

def attribute_is_valid(attribute, key):
    """
    Method to return if the attribute is valid
    :param attribute:
    :param key:
    :return:
    """
    return attribute.lower().startswith(key)

def replace_unwanted_xml_attrs(body):
    """
    Method to return transformed string after removing all the unwanted characters from given xml body
    :param body:
    :return:
    """
    return body.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
