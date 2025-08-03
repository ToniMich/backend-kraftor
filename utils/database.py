import json
import os
from threading import Lock

class JSONDatabase:
    """
    A simple file-based JSON database.
    Stores collections as top-level keys, each mapping to a dict of items.
    """
    def __init__(self, filepath: str):
        self.filepath = filepath
        self._lock = Lock()
        self.data = {}

    def load(self) -> None:
        """
        Load database from the JSON file, or initialize empty if not present.
        """
        with self._lock:
            if os.path.exists(self.filepath):
                with open(self.filepath, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
            else:
                self.data = {}

    def save(self) -> None:
        """
        Save current database state to the JSON file.
        """
        with self._lock:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)

    def get(self, collection: str, key: str):
        """
        Retrieve a single item by collection and key, or None if not found.
        """
        return self.data.get(collection, {}).get(key)

    def get_all(self, collection: str):
        """
        Retrieve all items in a collection as a list of dicts.
        """
        return list(self.data.get(collection, {}).values())

    def set(self, collection: str, key: str, value: dict) -> None:
        """
        Set or update an item in a collection, then persist to disk.
        """
        with self._lock:
            if collection not in self.data:
                self.data[collection] = {}
            self.data[collection][key] = value
            self.save()

