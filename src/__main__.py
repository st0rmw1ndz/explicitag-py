import sys

from loguru import logger

from .cli import main


def setup_log_handlers() -> None:
    """Sets up the logging configuration, like output format and level."""
    logger.remove()
    logger.add(
        sys.stdout,
        format="[{time:HH:mm:ss}] {level} - {message}",
        level="INFO",
    )


if __name__ == "__main__":
    setup_log_handlers()
    sys.exit(main())
