import argparse

from constants import EXPORT_CHOICES, DEFAULT_COMMIT_COUNT


def parse_arguments():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    parser.add_argument('-e', '--export', choices=EXPORT_CHOICES, help='Parsed git log is exported in this format', required=True)
    parser.add_argument('-n', '--log-count', type=int, help='Number of commits to be parsed', default=DEFAULT_COMMIT_COUNT)
    group.add_argument('-f', '--file-path', type=str, help='File path containing git log contents')
    group.add_argument('-d', '--directory', type=str, help='Directory from which git log should be extracted')
    return parser.parse_args()


if __name__ == '__main__':
    arguments = parse_arguments()
