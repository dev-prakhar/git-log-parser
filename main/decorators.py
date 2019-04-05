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
