import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler


def log_filesystem_change(path="."):
    """Logs filesystem changes in the specified directory.

    Args:
        path (str): Directory path to monitor. Defaults to current directory.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    event_handler = LoggingEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while observer.isAlive():
            observer.join(1)
    finally:
        observer.stop()
        observer.join()
