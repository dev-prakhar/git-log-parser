# ------------------------------------------------- parse.py -----------------------------------------------------------

CSV_EXPORT = 'csv'
JSON_EXPORT = 'json'
EXPORT_CHOICES = (CSV_EXPORT, JSON_EXPORT,)
DEFAULT_COMMIT_COUNT = 5

# -------------------------------------------------- utils.py ----------------------------------------------------------

GIT_LOG_COMMAND = 'git -C {dir} log -n {number}'
GIT_VALID_DIRECTORY_COMMAND = 'git -C {dir} rev-parse --is-inside-work-tree'
NON_ZERO_CODE_ERROR = 'Invalid command entered via terminal'

# ------------------------------------------------ parser.py -----------------------------------------------------------

COMMIT = 'commit'
MERGE = 'merge'
AUTHOR = 'author'
DATE = 'date'
MESSAGE = 'message'

PARSING_ERROR = 'Error due to parsing git log'
PARSING_SUCCESS = 'Successfully parsed entries to git-log.{file}'

# ----------------------------------------------------------------------------------------------------------------------