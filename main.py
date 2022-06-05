from collections import UserDict


class Field:
    def __init__(self, value) -> None:
        self.value = value

    def __str__(self) -> str:
        return f'{self.value}'


class Name(Field):
    pass


class Phone(Field):
    pass


class Record:
    def __init__(self, name: Name, phones=[]) -> None:
        self.name = name
        self.phone_list = phones

    def __str__(self) -> str:
        return f'User {self.name} - Phones: {", ".join([phone.value for phone in self.phone_list])}'

    def add_phone(self, phone: Phone) -> None:
        self.phone_list.append(phone)

    def del_phone(self, phone: Phone) -> None:
        self.phone_list.remove(phone)

    def edit_phone(self, phone: Phone, new_phone: Phone) -> None:
        self.phone_list.remove(phone)
        self.phone_list.append(new_phone)


class AddressBook(UserDict):
    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record


class InputError:
    def __init__(self, func) -> None:
        self.func = func

    def __call__(self, contacts, *args):
        try:
            return self.func(contacts, *args)
        except IndexError:
            return 'Sorry,enter command,name,phone'
        except KeyError:
            return 'Sorry,user not found, try again!'
        except ValueError:
            return 'Sorry,phone number not found,try again!'


def greeting(*args):
    return 'Hello! Can I help you?'


@InputError
def add(contacts, *args):
    name = Name(args[0])
    phone = Phone(args[1])
    if name.value in contacts:
        contacts[name.value].add_phone(phone)
        return f'Add phone number: {phone} for {name}'
    else:
        contacts[name.value] = Record(name, [phone])
        return f'Add {name}:{phone}'


@InputError
def change(contacts, *args):
    name, old_phone, new_phone = args[0], args[1], args[2]
    contacts[name].edit_phone(Phone(old_phone), Phone(new_phone))
    return f'{name} your old phone number: {old_phone} was changed to {new_phone}'


@InputError
def phone(contacts, *args):
    name = args[0]
    phone = contacts[name]
    return f'{phone}'


@InputError
def del_phone(contacts, *args):
    name, phone = args[0], args[1]
    contacts[name].del_phone(Phone(phone))
    return f'for {name} {phone} is delete'


def show_all(contacts, *args):
    for key in contacts:
        return f'{contacts[key]}'


def exiting(*args):
    return 'Good bye!'


COMMANDS = {greeting: ['hello'], add: ['add'], change: ['change'], phone: ['phone'],
            show_all: ['show'], exiting: ['good bye', 'close', 'exit'],
            del_phone: ['delete']}


def command_parser(user_command: str) -> str:
    for key, list_value in COMMANDS.items():
        for value in list_value:
            if user_command.lower().startswith(value):
                args = user_command[len(value):].split()
                return key, args


def main():
    contacts = AddressBook()
    while True:
        user_command = input('>>> ')
        command, data = command_parser(user_command)
        print(command(contacts, *data))
        if command is exiting:
            break


if __name__ == '__main__':
    main()
