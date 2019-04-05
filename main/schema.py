class GitCommit:
    """
    Model to represent a single git __commit entry
    """
    COMMIT_ENTRY_CSV_FORMAT = '{0.__commit}, {0.__merge}, {0.__author}, {0.__date}, {0.__message}'

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
        Representation of commit entry in csv
        """
        return self.COMMIT_ENTRY_CSV_FORMAT.format(self)
