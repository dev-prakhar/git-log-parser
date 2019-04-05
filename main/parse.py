import argparse

from constants import EXPORT_CHOICES, DEFAULT_COMMIT_COUNT
from parser import Parser


def parse_arguments():
    """
    Method to parse the command line arguments
    :return: Dictionary of parsed arguments
    """

    def add_arg(*args, **kwargs):
        parser.add_argument(*args, **kwargs)

    def add_group_arg(*args, **kwargs):
        group.add_argument(*args, **kwargs)

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    add_arg('-e', '--export', choices=EXPORT_CHOICES, help='Parsed git log is exported in this format', required=True)
    add_arg('-n', '--log-count', type=int, help='Number of commits to be parsed', default=DEFAULT_COMMIT_COUNT)
    add_group_arg('-f', '--file-path', type=str, help='File path containing git log contents')
    add_group_arg('-d', '--directory', type=str, help='Directory from which git log should be extracted')
    return parser.parse_args().__dict__


if __name__ == '__main__':
    arguments = parse_arguments()
    Parser(**arguments).delegate()
