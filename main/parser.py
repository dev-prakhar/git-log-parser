import json

from constants import COMMIT, MERGE, AUTHOR, DATE, MESSAGE, JSON_EXPORT, PARSING_ERROR, PARSING_SUCCESS
from decorators import catch_exception
from exceptions import GitLogParsingException
from loggers import Logger
from schema import GitCommit
from utils import get_git_log_contents, get_string_after_n_space, get_cleaned_log


class Parser(object):
    def __init__(self, export, file_path, directory, log_count):
        self.export = export
        self.file_path = file_path
        self.directory = directory
        self.log_count = log_count

    @catch_exception
    def delegate(self):
        parsed_objects = None
        if self.file_path:
            parsed_objects = FileParser(self.file_path, self.log_count).parse()
        elif self.directory:
            parsed_objects = DirectoryParser(self.directory, self.log_count).parse()

        if parsed_objects:
            Export(git_commits=parsed_objects, export_to=self.export).export()
            Logger.log(PARSING_SUCCESS.format(file=self.export))
        else:
            raise GitLogParsingException(PARSING_ERROR)


class FileParser:
    def __init__(self, file_path, log_count):
        self.file_path = file_path
        self.log_count = log_count

    def parse(self):
        pass


class DirectoryParser:
    def __init__(self, directory, log_count):
        self.directory = directory
        self.log_count = log_count

    def parse(self):
        git_log_contents = get_git_log_contents(directory=self.directory, log_count=self.log_count)
        return EntryParser(git_log_contents).parse()


class EntryParser:
    def __init__(self, git_log):
        self.git_log = git_log
        self.entries = []

    def parse(self):
        self.create_entries()
        return [GitCommit(**entry) for entry in self.entries]

    def create_entries(self):
        for log in self.git_log:
            log_attributes = get_cleaned_log(log.splitlines())
            merge, author_index, date_index = self.get_merge_and_indexes(log_attributes)
            entry = {
                COMMIT: get_string_after_n_space(log_attributes[0], 1),
                MERGE: merge,
                AUTHOR: get_string_after_n_space(log_attributes[author_index], 1),
                DATE: get_string_after_n_space(log_attributes[date_index], 1),
                MESSAGE: '\n'.join(log_attributes[date_index+1:])
            }
            self.entries.append(entry)

    def get_merge_and_indexes(self, log_attributes):
        author_index = 1
        date_index = 2
        merge = ''
        log_attribute = log_attributes[1]
        if log_attribute.lower().startswith(MERGE):
            author_index += 1
            date_index += 1
            merge = get_string_after_n_space(log_attribute, 1)
        return merge, author_index, date_index


class Export:
    def __init__(self, git_commits, export_to):
        self.git_commits = git_commits
        self.export_to = export_to

    def export(self):
        return self.to_json() if self.export_to == JSON_EXPORT else self.to_csv()

    def to_json(self):
        commits = [commit.to_json() for commit in self.git_commits]
        with open('git-log.json', 'a') as git_log_file:
            git_log_file.write(json.dumps(commits))

    def to_csv(self):
        pass