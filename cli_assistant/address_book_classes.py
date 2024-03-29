from collections import UserDict
from datetime import datetime
import pickle
from pathlib import Path
import re


class Field:
    def __init__(self, value):
        self._value = value

    def __str__(self):
        return self._value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class Name(Field):
    def __str__(self):
        return self._value.title()


class Phone(Field):
    @staticmethod
    def validate_phone(phone):
        new_phone = (
            str(phone)
            .strip()
            .replace("+", "")
            .replace(" ", "")
            .replace("(", "")
            .replace(")", "")
            .replace("-", "")
        )
        if not new_phone.isdigit():
            raise ValueError("The phone number should contain only numbers!")
        else:
            if len(new_phone) == 10:
                return f"{new_phone}"
            else:
                raise ValueError("Check the length of the phone number!")

    def __init__(self, value):
        self._value = Phone.validate_phone(value)

    @Field.value.setter
    def value(self, value):
        self._value = Phone.validate_phone(value)


class Email(Field):
    @staticmethod
    def validate_email(email):
        pattern = r"^[-\w\.]+@([-\w]+\.)+[-\w]{2,}$"
        if re.match(pattern, email) is not None:
            return f"{email}"
        else:
            raise ValueError("Email is not correct!")

    def __init__(self, value):
        self._value = Email.validate_email(value)

    @Field.value.setter
    def value(self, value):
        self._value = Email.validate_email(value)


class Address(Field):
    def __str__(self):
        return self._value


class Birthday(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        try:
            if value != None:
                self._value = datetime.strptime(value, "%d/%m/%Y").date()
        except ValueError:
            print(f"Please, input the date in format dd/mm/yyyy ")


class Record:
    def __init__(self, name, phone=None, email=None, birthday=None, address=None):
        self.name = name
        self.birthday = birthday
        self.address = address

        self.emails = []
        if email:
            self.emails.append(email)

        self.phones = []
        if phone:
            self.phones.append(phone)

    """Робота з phone"""

    def add_phone(self, phone):
        phone = Phone(phone)
        self.phones.append(phone)

    def change_phone(self, old_phone, new_phone):
        old_phone = Phone(old_phone)
        new_phone = Phone(new_phone)
        for phone in self.phones:
            if phone.value == old_phone.value:
                phone.value = new_phone.value

    def delete_phone(self, old_phone):
        old_phone = Phone(old_phone)
        for phone in self.phones:
            if phone.value == old_phone.value:
                self.phones.remove(phone)

    """Робота з e-mail"""

    def add_email(self, email):
        email = Email(email)
        self.emails.append(email)

    def change_email(self, old_email, new_email):
        old_email = Email(old_email)
        new_email = Email(new_email)
        for email in self.emails:
            if email.value == old_email.value:
                email.value = new_email.value

    def delete_email(self, old_email):
        old_email = Email(old_email)
        for email in self.emails:
            if email.value == old_email.value:
                self.emails.remove(email)

    """Робота з датою народження"""

    def add_birthday(self, birthday):
        """Adding date of birth"""
        birthday = Birthday(birthday)
        self.birthday = birthday

    def delete_birthday(self):
        """Delete date of birth"""
        self.birthday = None

    def days_to_birthday(self):
        """How many days until user's birthday"""
        if self.birthday.value:
            try:
                birthday_value = datetime.strptime(
                    self.birthday.value, "%d/%m/%Y"
                ).date()
                current_date = datetime.now().date()
                user_date = birthday_value.replace(year=current_date.year)
                self.delta_days = user_date - current_date

                if 0 < self.delta_days.days:
                    return f"\n{self.name}'s birthday will be in {self.delta_days.days} days.\n"
                else:
                    user_date = birthday_value.replace(year=user_date.year + 1)
                    self.delta_days = user_date - current_date
                    if 0 < self.delta_days.days:
                        return f"\n{self.name}'s birthday will be in {self.delta_days.days} days.\n"
            except ValueError:
                return f"\nPlease, input date in format dd/mm/yyyy\n "
        else:
            return f"\nDate of birth is not found. Please, add day of birth, if you want.\n "

    """Робота з адресою"""

    def add_address(self, address):
        address = Address(address)
        self.address = address

    def delete_address(self):
        self.address = None

    def contacts(self):
        phon = []
        result_phones = ""
        result_emails = ""
        if len(self.phones) > 0:
            for i in self.phones:
                phon.append(str(i))
                result_phones = ", ".join(phon)
        em = []
        if len(self.emails) > 0:
            for i in self.emails:
                em.append(str(i))
                result_emails = ", ".join(em)
        return (
            f"\nname: {str(self.name.value)};\n"
            f"phone: {result_phones};\n"
            f"e-mail: {result_emails};\n"
            f"birthday: {self.birthday};\n"
            f"address: {self.address};\n"
            "==================="
        )


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def show_book(self):
        result = ""
        for name, value in self.data.items():
            s = f"{name}\n{value.contacts()}\n"
            result += s
        return result

    def del_record(self, name):
        self.data.pop(name)

    def search_contact(self, user_search):
        """search for contacts based on the user's search query"""
        counter = 0
        for value in self.data.values():
            result = str(value.contacts()).lower().find(user_search)
            if result != -1:
                counter += 1
                print(value.contacts())
        if counter == 0:
            return f"No data was found for your request. "

    def get_birthdays_per_range(self, range_of_days=7):
        """a list of users who have a birthday coming up soon"""

        near_birthdays = {}
        current_date = datetime.now().date()
        for name, value in self.data.items():
            if value.birthday:
                user_date = value.birthday.value
                user_date = datetime.strptime(user_date, "%d/%m/%Y").date()
                user_date = user_date.replace(year=current_date.year)
                delta_days = user_date - current_date

                if 0 < delta_days.days <= range_of_days:
                    near_birthdays.update({name: user_date})

                else:
                    user_date = user_date.replace(year=user_date.year + 1)
                    delta_days = user_date - current_date
                    if 0 < delta_days.days <= range_of_days:
                        near_birthdays.update({name: user_date})

                    elif 0 < delta_days.days > range_of_days:
                        continue

        print(f"\nNear birthdays for next {range_of_days} days:")
        sorted_near_birthdays = dict(
            sorted(near_birthdays.items(), key=lambda item: item[1])
        )
        result = ""
        for key, value in sorted_near_birthdays.items():
            s = f"{key}'s birthday will be on {str(value)}\n"
            result += s
        return result


p = Path("address_book.bin")
address_book = AddressBook()

if p.exists():
    with open("address_book.bin", "rb") as file:
        address_book.data = pickle.load(file)
