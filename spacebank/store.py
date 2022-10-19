import os
class BaseStore:
    _store = {}
    store_filename = None
    def __init__(self, store_filename):
        if not os.path.exists(store_filename):
            raise FileNotFoundError(f"Store '{filename}' does not exist")
        self.store_filename = store_filename
        self._read_store()
    
    def _read_store():
        pass

    def __repr__(self):
        return f"<BaseStore containing {len(self._store)} entries>"
    
    def __getitem__(self, val):
        if type(val) != str:
            raise ValueError("Invalid slice")
        if val not in self._store:
            raise KeyError(val)
        return self._store[val]