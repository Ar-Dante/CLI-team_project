import pickle
from pathlib import Path
from prompt_toolkit import prompt
from prompt_toolkit.completion import NestedCompleter
from .clean_folder import create_folders, sort_files, delete_folders, unpack_archives
from .exceptions import *
from .currency import *
from .main_information import *


def save_to_pickle():
    """Save address book in pickle file"""

    with open("address_book.bin", "wb") as fh:
        pickle.dump(address_book.data, fh)


def say_hello(s=None):
    return "\nHow can I help you?\n"


def say_goodbye(s=None):
    return "\nGood bye!\n"


@input_error
def new_note(text):
    note_ = RecordNote(text)
    nb.add_new_note(note_)
    nb.save_to_file()
    return f"\nThe note was created.\n"


@input_error
def ed_note(value):
    id_, text = value.split(" ", 1)
    nb.to_edit_text(id_, text)
    nb.save_to_file()
    return f"\nThe note was changed.\n"


@input_error
def tags(value):
    id_, *tags_ = value.split()
    nb.to_add_tags(id_, list(tags_))
    nb.save_to_file()
    return f"\nTags for note id:{id_} was added.\n"


@input_error
def sh_notes(value):
    return NotebookInfo.get_info(value)


@input_error
def del_notes(id_):
    nb.to_remove_note(id_)
    nb.save_to_file()
    return f"\nNote ID: {id_} was delete.\n"


@input_error
def search_n(text_to_search):
    return nb.search_note(text_to_search)


@input_error
def search_t(tag_to_search):
    return nb.search_tag(tag_to_search)


@input_error
def note(id_):
    return NoteInfo.get_info(id_)


@input_error
def get_curr(value):
    currency = value.strip().upper()
    if currency.isalpha():
        return get_currency(currency)
    else:
        return "\nYou need write command in format 'currency <name of currency>'\n"


@input_error
def add_contact(value):
    """Add new contact to address book"""

    name, *phones = value.lower().title().strip().split()
    name = Name(name.lower().title())

    if name.value not in address_book:
        record = Record(name)
        address_book.add_record(record)
        if phones:
            for phone in phones:
                record.add_phone(phone)
        save_to_pickle()
        return f"\nContact {name.value.title()} was created.\n"
    else:
        return f"\nContact {name.value.title()} already exists.\n"


@input_error
def show_all(s):
    """Функція виводить всі записи в телефонній книзі"""
    return AddressBookInfo.get_info(s)


@input_error
def remove_contact(name: str):
    """Функція для видалення контакта з книги"""

    record = address_book[name.strip().lower().title()]
    address_book.del_record(record.name.value)
    save_to_pickle()
    return f"\nContact {name.title()} was removed.\n"


@input_error
def add_phone(value):
    """Функція для додавання телефону контакта"""

    name, phone = value.lower().strip().title().split()

    if name.title() in address_book:
        address_book[name.title()].add_phone(phone)
        save_to_pickle()
        return f"\nThe phone number for {name.title()} was recorded.\n"
    else:
        return f"\nContact {name.title()} does not exist.\n"


@input_error
def remove_phone(value):
    """Функція для видалення телефону контакта"""
    name, phone = value.lower().title().strip().split()

    if name.title() in address_book:
        address_book[name.title()].delete_phone(phone)
        save_to_pickle()
        return f"\nPhone for {name.title()} was delete.\n"
    else:
        return f"\nContact {name.title()} does not exist.\n"


@input_error
def change_ph(value: str):
    """Функція для заміни телефону контакта"""

    name, old_phone, new_phone = value.split()

    if name.strip().lower().title() in address_book:
        address_book[name.strip().lower().title()].change_phone(old_phone, new_phone)
        save_to_pickle()
    else:
        return f"\nContact {name.title()} does not exists\n"


@input_error
def contact(value):
    """Функція відображає дані абонента, по імені або номеру телефона"""
    return ContactInfo.get_info(value)


@input_error
def add_em(value):
    """Функція для додавання e-mail контакта"""

    name, email = value.split()
    name = name.title()
    if name.title() in address_book:
        address_book[name.title()].add_email(email)
        save_to_pickle()
        return f"\nThe e-mail for {name.title()} was recorded.\n"
    else:
        return f"\nContact {name.title()} does not exist.\n"


@input_error
def remove_em(value):
    """Функція для видалення e-mail контакта"""

    name, email = value.split()
    name = name.title()
    email = email.lower()
    if name.title() in address_book:
        address_book[name.title()].delete_email(email)
        save_to_pickle()
        return f"\nThe e-mail for {name.title()} was delete.\n"
    else:
        return f"\nContact {name.title()} does not exist.\n"


@input_error
def change_em(value: str):
    """Функція для заміни e-mail контакта"""

    name, old_em, new_em = value.split()

    if name.strip().lower().title() in address_book:
        address_book[name.strip().lower().title()].change_email(old_em, new_em)
        save_to_pickle()
        return f"\nThe e-mail for {name.title()} was changed.\n"
    else:
        return f"\nContact {name.title()} does not exists.\n"


@input_error
def add_adrs(value):
    """Функція для додавання адреси контакта"""

    name, address = value.split(" ", 1)
    name = name.title()
    if name.title() in address_book:
        address_book[name.title()].add_address(address)
        save_to_pickle()
        return f"\nThe address for {name.title()} was recorded.\n"
    else:
        return f"\nContact {name.title()} does not exist.\n"


@input_error
def change_adrs(value):
    """Функція для зміни адреси контакта"""

    name, address = value.split(" ", 1)
    name = name.title()
    if name.strip().lower().title() in address_book:
        address_book[name.title()].add_address(address)
        save_to_pickle()
        return f"\nThe address for {name.title()} was changed.\n"
    else:
        return f"\nContact {name.title()} does not exists.\n"


@input_error
def remove_adrs(value):
    """Функція для видалення адреси контакта"""

    name = value.lower().title().strip()
    if name.title() in address_book:
        address_book[name.title()].delete_address()
        save_to_pickle()
        return f"\nAddress for {name.title()} was delete.\n"
    else:
        return f"\nContact {name.title()} does not exist.\n"


@input_error
def remove_bd(value):
    """Функція для видалення дня народження контакта контакта"""

    name = value.lower().title().strip()

    if name.title() in address_book:
        address_book[name.title()].delete_birthday()
        save_to_pickle()
        return f"\nBirthday for {name.title()} was delete.\n"
    else:
        return f"\nContact {name.title()} does not exist.\n"


@input_error
def add_contact_birthday(value):
    """Функція для додавання дня народження контакта к книгу"""

    name, birthday = value.lower().strip().split()

    if name.title() in address_book:
        address_book[name.title()].add_birthday(birthday)
        save_to_pickle()
        return f"\nThe Birthday for {name.title()} was recorded.\n"
    else:
        return f"\nContact {name.title()} does not exists.\n"


@input_error
def days_to_bd(name):
    """Функція виводить кількість днів до дня народження контакта"""

    if name.title() in address_book:
        if not address_book[name.title()].birthday is None:
            days = address_book[name.title()].days_to_birthday()
            return days
        else:
            return f"\n{name.title()}'s birthday is unknown.\n"
    else:
        return f"\nContact {name.title()} does not exists.\n"


@input_error
def get_birthdays(value=None):
    """Функція виводить перелік іменинників за період"""

    if value.strip() == "":
        period = 7
    else:
        period = int(value.strip())
    return address_book.get_birthdays_per_range(period)


@input_error
def change_bd(value):
    """Функція для зміни дня народження контакта"""

    name, new_birthday = value.lower().strip().split()
    if name.title() in address_book:
        address_book[name.title()].delete_birthday()
        address_book[name.title()].add_birthday(new_birthday)
        save_to_pickle()
        return f"\nBirthday for {name.title()} was changed.\n"
    else:
        return f"\nContact {name.title()} does not exist.\n"


@input_error
def search(text_to_search: str):
    """Search contact where there is 'text_to_search'"""
    return ContactInfo.get_info(text_to_search)


@input_error
def add_the_task(value):
    """Функція для додавання завдання в книгу завдань"""

    try:
        name, deadline, text = value.lower().strip().split(" ", 2)
        user = ResponsiblePerson(name)
        task = Task(text, user, deadline)
        tasklist.add_task(task)
        tasklist.save_to_file()
    except ValueError:
        f"\nPlease white command in format 'add task <name> <deadline in format: YYYY-m-d> <task>'\n"
    else:
        return f"\nThe task was created.\n"


@input_error
def remove_the_task(value):
    """Функція для видалення завдання з книги завдань"""

    try:
        Id = int(value.strip())
    except TypeError:
        f"\nPlease white command in format 'remove task <ID>'\n"
    else:
        tasklist.remove_task(Id)
        tasklist.save_to_file()
        return f"\nThe task was delete\n"


@input_error
def show_tasks(value):
    """Функція виводить перелік всіх завдань"""
    return TaskbookInfo.get_info(value)


@input_error
def change_d_line(value):
    """Функція змінює дедлайн завдання"""

    Id, new_deadline = value.split()
    try:
        Id = int(Id)
    except TypeError:
        f"\nPlease white command in format 'change deadline <ID> <new deadline>'\n"
    else:
        if Id in tasklist.task_lst:
            tasklist.change_deadline(Id, new_deadline)
            tasklist.save_to_file()
    return f"\nDeadline for task ID: {Id} was changed.\n"


@input_error
def search_in_task(text_to_search: str):
    """Шукаємо завдання по тексту"""

    text = text_to_search.strip().lower()
    return tasklist.search_task(text)


@input_error
def search_responce(name):
    """Шукаємо завдання по виконавцю"""

    name = name.strip().lower()
    return tasklist.search_respons_person(name)


@input_error
def well_done(id):
    return tasklist.set_done(id)


@input_error
def clean_f(path):
    """функція викликає функції що відповідають за сортування файлів в вибраній теці"""
    p = Path(path)
    try:
        create_folders(p)
    except FileNotFoundError:
        print(
            "\nThe folder was not found. Check the folder's path and run the command again!.\n"
        )
    else:
        sort_files(p)
        delete_folders(p)
        unpack_archives(p)
        return "Done\n"


def helps(value):
    return AllCommandInfo.get_info(value)


def short_help(value):
    return InfoHelper.get_info(value)


handlers = {
    "add note": new_note,
    "change note": ed_note,
    "add tags": tags,
    "show notes": sh_notes,
    "remove note": del_notes,
    "search notes": search_n,
    "search tags": search_t,
    "note": note,
    "hello": say_hello,
    "good bye": say_goodbye,
    "close": say_goodbye,
    "exit": say_goodbye,
    "currency": get_curr,
    "short help": short_help,
    "help": helps,
    "add contact": add_contact,
    "remove contact": remove_contact,
    "show addressbook": show_all,
    "add phone": add_phone,
    "remove phone": remove_phone,
    "change phone": change_ph,
    "add email": add_em,
    "remove email": remove_em,
    "change email": change_em,
    "phone": contact,
    "add birthday": add_contact_birthday,
    "remove birthday": remove_bd,
    "change birthday": change_bd,
    "days to birthday": days_to_bd,
    "birthdays": get_birthdays,
    "change address": change_adrs,
    "remove address": remove_adrs,
    "add address": add_adrs,
    "add task": add_the_task,
    "remove task": remove_the_task,
    "show tasks": show_tasks,
    "change deadline": change_d_line,
    "search tasks": search_in_task,
    "responsible person": search_responce,
    "search contacts": search,
    "clean-folder": clean_f,
    "done": well_done,
}

completer = NestedCompleter.from_nested_dict(
    {
        "add": {
            "contact": {"<name> <phone> <phone> ... <phone>"},
            "phone": {"<name> <one phone>"},
            "email": {"<name> <e-mail>"},
            "address": {"<name> <address>"},
            "birthday": {"<name> <d/m/yyyy>"},
            "note": {"<text>"},
            "tags": {"<id> <tag1 tag2 tag3...>"},
            "task": {"<name> <d/m/yyyy> <text of task>"},
        },
        "remove": {
            "contact": {"<name>"},
            "phone": {"<name> <old phone>"},
            "email": {"<name>"},
            "address": {"<name>"},
            "birthday": {"<name>"},
            "note": {"<id>"},
            "task": {"<ID of task>"},
        },
        "change": {
            "phone": {"<name> <old phone> <new phone>"},
            "email": {"<name> <new e-mail>"},
            "birthday": {"<name> <d/m/yyyy>"},
            "address": {"<name> <new address>"},
            "note": {"<id> <edited text>"},
            "deadline": {"<ID of task> <d/m/yyyy>"},
        },
        "phone": {"<name>"},
        "search": {
            "notes": {"<text_to_search>"},
            "tags ": {"<tag_to_search>"},
            "contacts": {"<text_to_seach>"},
            "tasks": {"<text_to_seach>"},
        },
        "good bye": None,
        "close": None,
        "exit": None,
        "show": {
            "addressbook": None,
            "notes": None,
            "tasks": None,
        },
        "note": {"<id>"},
        "days to birthday": {"<name>"},
        "birthdays": {"<number of days>"},
        "clean-folder": {"<path to folder>"},
        "hello": None,
        "help": None,
        "short help": None,
        "done": {"<ID of task>"},
        "responsible person": {"<name>"},
        "currency": {
            "USD": None,
            "EUR": None,
            "PLN": None,
            "GBP": None,
            "CZK": None,
            "CNY": None,
            "CAD": None,
        },
    }
)


def main():
    while True:
        command = prompt("Enter command: ", completer=completer)
        command = command.strip().lower()
        if command in ("exit", "close", "good bye", "."):
            say_goodbye()
            break
        else:
            for key in handlers:
                if key in command:
                    print(handlers[key](command[len(key) :].strip()))
                    break


if __name__ == "__main__":
    main()
