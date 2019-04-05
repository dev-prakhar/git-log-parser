import subprocess

def execute_command(command):
    """
    Method to execute command in shell
    :param command:
    """
    return subprocess.call(command, shell=True)

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
