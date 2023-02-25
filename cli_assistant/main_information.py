from abc import abstractmethod, ABC
import pyttsx3
from .address_book_classes import *
from .note_book_classes import *
from .task_list_classes import *


class Info(ABC):
    @abstractmethod
    def get_info(data):
        pass


class ContactInfo(Info):
    def get_info(text_to_search:str):
        text_to_search = text_to_search.strip()
        if text_to_search[0].isalpha():
            name = text_to_search.title()
            if name and name.title() in address_book:
                record = address_book[name.title()]
                return record.contacts()
            else:
                return f"\nContact {name.title()} does not exist.\n"

        elif text_to_search[0].isdigit() or text_to_search[0] in ("+", "(") and text_to_search[1].isdigit():
            phone = Phone.validate_phone(text_to_search)
            for record in address_book.values():
                lst = [phone.value for phone in record.phones]
                if phone in lst:
                    return record.contacts()
                else:
                    return f"\nContact with phone number {text_to_search} does not exist.\n"


class AddressBookInfo(Info):
    def get_info(data):
        if len(address_book) == 0:
            return "\nPhone book is empty.\n"
        else:
            result = "\n"
            for name, value in address_book.data.items():
                s = f"{name}\n{value.contacts()}\n"
                result += s
            return result


class NoteInfo(Info):
    def get_info(id):
        try:
            s = pyttsx3.init()
            text_to_speach = nb.notes[int(id)].note
            s.say(text_to_speach)
            s.runAndWait()
        except ValueError:
            "Sound is not available"
        finally:
            return nb.show_note(id)


class NotebookInfo(Info):
    def get_info(data):
        if len(nb.notes) > 0:
            result = "\n"
            for id_, rec in nb.notes.items():
                tgs = [tg.word.lower() for tg in rec.tags]
                tags = ", ".join(tgs)
                date = rec.date
                result += f"\nid: {id_}      date: {date} \n{rec.note}\ntags: {tags} \n=========\n"
            return result
        else:
            return f"\nNotebook is empty.\n"


class TaskbookInfo(Info):
    def get_info(data):
        result = '\n'
        if len(tasklist.task_lst) > 0:
            for k, v in tasklist.task_lst.items():
                result += f"=== ID: {k} === {v.see_task()}\n"
            return result
        else:
            return f"\nTask book is empty.\n"


class AllCommandInfo(Info):
    def get_info(data):
        rules = """LIST OF COMMANDS: \n
            1) to add new contact and one or more phones, write command: add contact <name> <phone> <phone> ... <phone>
        2) to remove contact, write command: remove contact <name>
        3) to add phone, write command: add phone <name> <one phone>
        4) to change phone, write command: change phone <name> <old phone> <new phone>
        5) to remove phone, write command: remove phone <name> <old phone>
        6) to add e-mail, write command: add email <name> <e-mail>
        7) to change e-mail, write command: change email <name> <new e-mail>
        8) to remove e-mail, write command: remove email <name>
        9) to add address, write command: add address <name> <address>
        10) to change address, write command: change address <name> <new address>
        11) to remove address, write command: remove address <name>
        12) to add birthday of contact, write command: add birthday <name> <dd/mm/yyyy>
        13) to remove birthday, write command: remove birthday <name>
        14) to change birthday, write command: change birthday <name> <d/m/yyyy>
        15) to see how many days to contact's birthday, write command: days to birthday <name>
        16) to see list of birthdays in period, write command: birthdays <number of days>
        17) to search contact, where is 'text', write command: search contact <text>
        18) to see full record of contact, write: phone <name>
        19) to see all contacts, write command: show addressbook
        20) to say goodbye, write one of these commands: good bye / close / exit / . 
        21) to say hello, write command: hello
        22) to see help, write command: help

        23) to sort file in folder, write command: clean-folder <path to folder>

        24) to add note use command: add note <text>
        25) to change note use command: change note <id> <edited text>
        26) to add tags use command: add tags <id> <tag1 tag2 tag3...>
        27) to show all notes use command: show notes
        28) to show any note use command: note <id>
        29) to remove note use command: remove note <id>
        30) to search notes use command: search notes <text_to_search>
        31) to search tags use command: search tags <tag_to_search>

        32)  to add task use command: add task <name of responsible persons> <deadline in format dd/mm/yyyy> <text of task>
        33) to remove task use command: remove task <ID of task>
        34) to see all tasks use command: show tasks
        35) to change deadline of task use command: change deadline <ID of task> <new deadline in format dd/mm/yyyy>
        36) to search tasks use command: search tasks <text_to_search>
        37) to search tasks of responsible person use command: responsible person <name>
        38) to set status of task "done" use command: done <ID of tasl>
        39) to see rate of currency use command: currency <name of currency>: 
        """
        return rules


class InfoHelper(Info):
    def get_info(data):
        commands = """
        You can use commands:
        - help - hello - good bye - close - exit - . 
        - currency
        - clean-folder  
        ADDRESS BOOK:
        - show addressbook - search contacts - phone
        - add contact - remove contact - add phone - change phone - remove phone 
        - add email - change email - remove email - add address - change address - remove address
        - add birthday - remove birthday - change birthday - days to birthday - birthdays
        NOTES BOOK:
        - show notes - note - search notes - search tags
        - add note - change note - remove note - add tags
        TASK BOOK:            
        - show tasks - search tasks - responsible person
        - add task - remove task - change deadline - done
        """

        return commands
