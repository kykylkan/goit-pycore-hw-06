from collections import UserDict
from dataclasses import dataclass
import re

PHONE_PATTERN = re.compile("\d{10}")


class ValidationException(Exception):
    pass


@dataclass
class Field:
    value: str

    def __str__(self) -> str:
        return str(self.value)


class Name(Field):
    def __init__(self, value: str) -> None:
        super().__init__(value)


class Phone(Field):
    def __init__(self, value: str) -> None:

        result = re.fullmatch(PHONE_PATTERN, value)

        if result == None:
            raise ValidationException("Phone should has 10 numbers")

        super().__init__(value)


class Record:
    def __init__(self, name: str) -> None:
        if not len(name):
            raise ValidationException("Enter the name")

        self.name = Name(name)
        self.phones: list[Record] = []

    # add phone object in list
    def add_phone(self, phone: str) -> None:
        self.phones.append(Phone(phone))

    # remove phone object from list
    def remove_phone(self, phone: str) -> bool:
        phoneIndex = None

        # find the phone position
        for key, item in enumerate(self.phones):
            if item.value == phone:
                phoneIndex = key
                break

        # remove phone by his position outside the loop
        if phoneIndex != None:
            del self.phones[phoneIndex]

            print(f"Phone {phone} was removed")
            return True

        print(f"Phone {phone} was not found")
        return False

    # update phone by number with a new one
    def edit_phone(self, original_phone: str, new_phone: str) -> bool:
        is_updated = False

        # manually go through the phones and update the correct one directly in phone object
        for key, item in enumerate(self.phones):
            if item.value == original_phone:
                self.phones[key].value = new_phone
                is_updated = True

                print(f"Phone {original_phone} was updated")
                break

        # I think this variant, is not good from in terms of perfomance
        # self.phones = list(map(lambda item: Phone(new_phone) if item.value == original_phone else Phone(item.value), self.phones))

        print(f"Phone {original_phone} was not updated")

        return is_updated

    # find and return phone(truthy) or False
    def find_phone(self, phone: str) -> str | bool:

        # in a huge list I think the best way it is a simple loop
        phoneItem = list(filter(lambda item: item.value == phone, self.phones))

        if len(phoneItem):
            return phoneItem.pop()

        print(f"Phone {phone} was not found")
        return False

    def __str__(self) -> str:
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


# store any record in book by user name
class AddressBook(UserDict):

    # store record
    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    # find record
    def find(self, name: str) -> Record | None:
        if name in self.data:
            return self.data[name]

    # delete record
    def delete(self, name: str) -> None:
        if name in self.data:
            del self.data[name]


if __name__ == "__main__":
    # testing...

    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # john_record2 = Record("")
    # john_record2.add_phone("666")

    print(john_record.find_phone("111111"))
    print(john_record.find_phone("5555555555"))

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")

    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john: Record = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    # Виведення: Contact name: John, phones: 1112223333; 5555555555
    print(john)

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("1112223333")
    print(f"{john.name}: {found_phone}")  # Виведення: 1112223333

    # Видалення запису Jane
    book.delete("Jane")

    john_record.remove_phone("5555555555")

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)
