import pickle
from datetime import datetime


def is_id_exist(func):
    """ Decorator checks if id exists and it saves changes to pickle-file """

    def wrapper(*args):
        id_ = args[1]
        if int(id_) in args[0].notes:
            result = func(*args)
            args[0].save_to_file()
            return result
        else:
            return f"\nThe note with ID: {id_} is not exists\n"
    return wrapper


class Tag:
    """Class for creating a tag"""

    def __init__(self, word):
        self.word = word.lower()


class RecordNote:
    """Class for creating a note"""

    def __init__(self, note: str):
        self.note = note
        self.tags = []
        self.date = datetime.now().date()

    def edit_text(self, text_):
        self.note = text_

    def add_tags(self, tags: list[str]):
        for tg in tags:
            self.tags.append(Tag(tg))

    def __del__(self):
        return f"\nThe Note was delete.\n"


class Notebook:
    """Class for creating notes"""

    counter = 0

    def __init__(self):
        self.notes = {}
        self.read_from_file()

    def add_new_note(self, note: RecordNote):
        self.notes[self.counter+1] = note
        self.counter += 1
        self.save_to_file()

    def read_from_file(self):
        try:
            with open("notes.bin", "rb") as fh:
                self.notes = pickle.load(fh)
                if self.notes:
                    self.counter = max(self.notes.keys())
        except FileNotFoundError:
            self.notes = {}
            self.counter = 0

    def save_to_file(self):
        with open("notes.bin", "wb") as fh:
            pickle.dump(self.notes, fh)

    @is_id_exist
    def to_edit_text(self, id_, text_):
        self.notes[int(id_)].edit_text(text_)

    @is_id_exist
    def to_add_tags(self, id_, tags: list[str]):
        self.notes[int(id_)].add_tags(tags)

    @is_id_exist
    def to_remove_note(self, id_):
        del self.notes[int(id_)]
        return f"\nThe note id:{id_} was delete!\n"

    @is_id_exist
    def show_note(self, id_):
        tgs = [tg.word.lower() for tg in self.notes[int(id_)].tags]
        tags = ", ".join(tgs)
        return f"\nid: {id_}     date: {self.notes[int(id_)].date} " \
               f"\n{self.notes[int(id_)].note}\ntags: {tags} \n========\n "

    def search_note(self, text_to_search: str):
        for id_, value in self.notes.items():
            if text_to_search.lower().strip() in value.note.lower():
                tgs = [tg.word for tg in value.tags]
                tags = ", ".join(tgs)
                result = f"=== id: {id_} ===   date: {value.date} \n{value.note}\ntags: {tags} \n========\n "
                print(result)

    def search_tag(self, tag_to_search: str):
        for id_, value in self.notes.items():
            tgs = [tg.word.lower() for tg in value.tags]
            if len(tgs) == 0:
                tgs = [""]
            if tag_to_search.lower().strip() in tgs:
                tags = ", ".join(tgs)
                result = f"id: {id_}    date: {value.date} \n{value.note}\ntags: {tags} \n========\n "
                print(result)


nb = Notebook()
