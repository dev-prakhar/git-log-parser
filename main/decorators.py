from constants import PARSING_ERROR
from exceptions import NonZeroExitCodeException, GitLogParsingException
from loggers import Logger


def catch_exception(func):
    """
    Decorator that catches exception and exits the code if needed
    """
    def exit_if_failed(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except (NonZeroExitCodeException, GitLogParsingException) as exception:
            Logger.error(exception.message)
            quit()
    return exit_if_failed


def raise_parsing_exception(func):
    """
    Decorator that throws Parsing exception if any exception is raised during parsing
    """
    def raise_if_failed(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except Exception:
            raise GitLogParsingException(PARSING_ERROR)
        else:
            return result
    return raise_if_failed
