from utils import replace_unwanted_xml_attrs


class GitCommit:
    """
    Model to represent a single git commit entry
    """
    def __init__(self, commit, author, date, message, merge=''):
        self.__commit = commit
        self.__merge = merge
        self.__author = author
        self.__date = date
        self.__message = message

    def to_json(self):
        """
        Representation of commit entry in json
        """
        commit_entry = {
            'commit': self.__commit,
            'merge': self.__merge,
            'author': self.__author,
            'date': self.__date,
            'message': self.__message
        }
        return commit_entry

    def to_csv(self):
        """
        Representation of commit entry as a csv row
        """
        return [self.__commit, self.__merge, self.__author, self.__date, self.__message]

    def to_xml(self):
        """
        Representation of commit entry in xml
        """

        def get_valid_xml_values():
            commit_entry = {
                'commit': replace_unwanted_xml_attrs(self.__commit),
                'merge': replace_unwanted_xml_attrs(self.__merge),
                'author': replace_unwanted_xml_attrs(self.__author),
                'date': replace_unwanted_xml_attrs(self.__date),
                'message': replace_unwanted_xml_attrs(self.__message)
            }
            return commit_entry

        return (
            "\t<item type='git_commit'>\n"
            "\t\t<commit>{commit}</commit>\n"
            "\t\t<merge>{merge}</merge>\n"
            "\t\t<author>{author}</author>\n"
            "\t\t<date>{date}</date>\n"
            "\t\t<message>{message}</message>\n"
            "\t</item>\n".format(**get_valid_xml_values())
        )
