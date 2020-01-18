from typing import List
from tinydb import TinyDB, Query


class PastebinDBService(object):
    def __init__(self):
        self.db = TinyDB('db.json')

    def create(self, pastebin_data_list):
        self.db.insert(pastebin_data_list)

    def add_bulk(self, pastebin_data_list):
        self.db.insert_multiple(pastebin_data_list)

    def get_existing_ids(self, ids: List[str]):
        paste = Query()
        search = self.db.search(paste.id.one_of(ids))
        return search
