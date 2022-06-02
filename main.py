from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value


class Name(Field):
    pass


class Phone(Field):
    pass


class Record:
    def __init__(self, name: Name, phone: Phone) -> None:
        self.name = name
        self.phone = phone


class AddressBook(UserDict):
    def add_record(self, rec: Record):
        self.data[rec.name.value] = rec


phone_book = AddressBook()


def input_error(func):
    def wrapper(*args):
        try:
            return func(*args)
        except IndexError:
            return 'Sorry,try again:command,name,phone.'
        except KeyError:
            return 'Name not found'
        except ValueError:
            return 'Value isn`t correct'

    return wrapper


@input_error
def exit(*args):
    return "Good bye!"


@input_error
def greeting(*args):
    return "Hello!"


@input_error
def add(*args):
    name = Name(args[0])
    phone = Phone(args[1])
    rec = Record(name, phone)
    phone_book.add_record(rec)
    return f'Contact {args[0]} add successful'


@input_error
def change_phone(*args):
    rec = phone_book[args[0]]
    return f'Contact {args[0]} changed'


@input_error
def show_all(*args):
    return '\n'.join(f'{key}: {value}' for key, value in phone_book.items())


@input_error
def remove(*args):
    for key in phone_book.keys():
        if key is args[0]:
            phone_book.pop(Record)
    return f'Contact {args[0]} was deleted'


COMMANDS = {exit: ["exit", "bye"], add: ["add", 'add contact'], show_all: ["show all", "show"],
            change_phone: ['change', 'change contact'], greeting: ['hello', 'hi'],
            remove: ['remove', 'delete']}


def parse_command(user_input: str):
    for k, v in COMMANDS.items():
        for i in v:
            if user_input.lower().startswith(i.lower()):
                return k, user_input[len(i):].strip().split(" ")


def main():
    while True:
        user_input = input(">>> ")
        result, data = parse_command(user_input)
        print(result(*data))
        if result is exit:
            break


if __name__ == "__main__":
    main()
