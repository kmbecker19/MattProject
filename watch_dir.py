import logging
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import (
    FileSystemEventHandler,
    FileCreatedEvent,
    FileModifiedEvent,
)
from filter_json import mangle_json_file


class CustomEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        if isinstance(event, FileCreatedEvent):
            self._handle_mangling(event)

    def on_modified(self, event):
        if isinstance(event, FileModifiedEvent):
            self._handle_mangling(event)

    def _handle_mangling(self, event):
        file_path = Path(event.src_path)
        if file_path.suffix in ('.json', '.jsonl'):
            filename = file_path.name
            data_dir = file_path.parent.parent
            output_dir = data_dir / "output"
            mangle_json_file(file_path, output_dir / filename, [])
            logging.info(
                f"Processed file '{file_path}' and saved to '{output_dir}'"
            )


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
    event_handler = CustomEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while observer.is_alive():
            observer.join(1)
    finally:
        observer.stop()
        observer.join()


if __name__ == "__main__":
    log_filesystem_change(path="./data/input")
