import csv
import json
from xml.dom.minidom import parseString

from dicttoxml import dicttoxml

from constants import COMMIT, MERGE, AUTHOR, DATE, MESSAGE, JSON_EXPORT, PARSING_ERROR, PARSING_SUCCESS, CSV_EXPORT, \
    XML_EXPORT
from decorators import catch_exception, raise_parsing_exception
from exceptions import GitLogParsingException
from loggers import Logger
from schema import GitCommit
from utils import git_log_via_command, get_string_after_n_space, get_cleaned_log, git_log_via_file, attribute_is_valid


class Parser(object):
    """
    Main Class that delegates the parsing to the respective class
    """
    def __init__(self, export, file_path, directory, log_count):
        self.export = export
        self.file_path = file_path
        self.directory = directory
        self.log_count = log_count

    @catch_exception
    def delegate(self):
        parsed_objects = None
        if self.file_path:
            parsed_objects = FileParser(self.file_path).parse()
        elif self.directory:
            parsed_objects = DirectoryParser(self.directory, self.log_count).parse()

        if parsed_objects:
            Exporter(git_commits=parsed_objects, export_to=self.export).export()
            Logger.log(PARSING_SUCCESS.format(file=self.export))
        else:
            raise GitLogParsingException(PARSING_ERROR)


class FileParser:
    """
    Parser that is used if file path is given
    """
    def __init__(self, file_path):
        self.file_path = file_path

    @raise_parsing_exception
    def parse(self):
        git_log_contents = git_log_via_file(file_path=self.file_path)
        return EntryParser(git_log_contents).parse()


class DirectoryParser:
    """
    Parser that is used if directory is given
    """
    def __init__(self, directory, log_count):
        self.directory = directory
        self.log_count = log_count

    def parse(self):
        git_log_contents = git_log_via_command(directory=self.directory, log_count=self.log_count)
        return EntryParser(git_log_contents).parse()


class EntryParser:
    """
    Parses each commit entry in git log
    """
    def __init__(self, git_log):
        self.git_log = git_log
        self.entries = []

    def parse(self):
        self.create_entries()
        return [GitCommit(**entry) for entry in self.entries]

    def create_entries(self):
        """
        Method responsible for creating git commit dict for every entry
        """
        for log in self.git_log:
            log_attributes = get_cleaned_log(log.splitlines())
            merge, author_index, date_index = self.get_merge_and_indexes(log_attributes)
            self.validate_entries(author_index, date_index, log_attributes)
            entry = {
                COMMIT: get_string_after_n_space(log_attributes[0], 1).split(' ')[0],
                MERGE: merge,
                AUTHOR: get_string_after_n_space(log_attributes[author_index], 1),
                DATE: get_string_after_n_space(log_attributes[date_index], 1),
                MESSAGE: '. '.join(log_attributes[date_index+1:])
            }
            self.entries.append(entry)

    def get_merge_and_indexes(self, log_attributes):
        """
        Returns value of merge attribute and author, date index on the basis of parsed merge attribute
        :param log_attributes:
        :return: merge, author_index, date_index
        """
        author_index = 1
        date_index = 2
        merge = ''
        log_attribute = log_attributes[1]
        if log_attribute.lower().startswith(MERGE):
            author_index += 1
            date_index += 1
            merge = get_string_after_n_space(log_attribute, 1)
        return merge, author_index, date_index

    def validate_entries(self, author_index, date_index, log_attributes):
        """
        Raises GitLogParsingError if any invalid entry is found
        :param author_index:
        :param date_index:
        :param log_attributes:
        """
        if not (
            attribute_is_valid(log_attributes[author_index], AUTHOR) and
            attribute_is_valid(log_attributes[date_index], DATE) and
            attribute_is_valid(log_attributes[0], COMMIT)
        ):
            raise GitLogParsingException(PARSING_ERROR)


class Exporter:
    """
    Class responsible for exporting to different files
    """
    def __init__(self, git_commits, export_to):
        self.git_commits = git_commits
        self.export_to = export_to

    def export_format(self):
        format_to_method_map = {
            JSON_EXPORT: self.to_json,
            CSV_EXPORT: self.to_csv,
            XML_EXPORT: self.to_xml
        }
        return format_to_method_map[self.export_to]

    def export(self):
        self.export_format()()

    def to_json(self):
        """
        Method to export the logs to a json file
        """
        commits = [commit.to_json() for commit in self.git_commits]
        with open('git-log.json', 'w') as git_log_file:
            git_log_file.write(json.dumps(commits, indent=4, separators=(',', ': ')))
        git_log_file.close()

    def to_csv(self):
        """
        Method to export the logs to a csv file
        """
        commits = [commit.to_csv() for commit in self.git_commits]
        with open('git-log.csv', 'w') as git_log_file:
            csv_writer = csv.writer(git_log_file)
            csv_writer.writerow(['Commit', 'Merge', 'Author', 'Date', 'Message'])
            csv_writer.writerows(commits)
        git_log_file.close()

    def to_xml(self):
        """
        Method to export the logs to an xml file
        """
        commits = [commit.to_json() for commit in self.git_commits]
        with open('git-log.xml', 'w') as git_log_file:
            raw_xml = dicttoxml(commits, attr_type=False, custom_root='git_log')
            pretty_xml = parseString(raw_xml).toprettyxml()
            git_log_file.write(pretty_xml)
        git_log_file.close()
