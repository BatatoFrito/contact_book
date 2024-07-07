"""

This program is a contact book through the terminal

"""

from pathlib import Path
from copy import deepcopy
import json
import os

def clear():
    return os.system('cls')

class ContactBook:
    def __init__(self, contacts: dict, json_file: Path) -> None:
        self.contacts = contacts
        self.json_file = json_file
        self.history = []
        self.contact_info = ['First Name', 'Last Name', 'E-mail', 'Phone']

    def add(self):
        temp_contact = {}
        for info in self.contact_info:
            clear()
            temp_info = input(f'{info}: ')
            temp_contact[info] = temp_info
        else:
            clear()

        confirmation = input('Are you sure you want to create this contact? (Y/N): ')[0].upper()
        if confirmation == 'Y':
            self.history.append(deepcopy(self.contacts))
            self.contacts['contacts'].append(temp_contact)
            json_contacts = json.dumps(self.contacts)
            with open(self.json_file, 'w+') as f:
                f.truncate(0)
                f.seek(0)
                f.write(json_contacts)
                f.seek(0)
        clear()


    def remove(self):
        clear()
        index = 1
        for contact in self.contacts['contacts']:
            print(f"{index} - {contact['First Name']} {contact['Last Name']}")
            index += 1
        to_delete = input('\nWhich contact would you like to delete? (ID Number): ')
        clear()
        confirmation = input('Are you sure you want to delete this contact?(Y/N): ')
        try:
            to_delete = int(to_delete)
        except(TypeError, IndexError):
            ...

    def edit():
        ...

    def see():
        ...

    def undo():
        ...


FILE_PATH = Path(__file__).absolute().parent
CONTACTS_PATH = FILE_PATH / 'contacts.json'

try:
    with open(CONTACTS_PATH, 'r') as f:
        data = json.load(f)
except(FileNotFoundError):
    with open(CONTACTS_PATH, 'w+') as f:
        f.write('{'
                '"contacts": ['
                    '{'
                        '"First Name": "Marcio",'
                        '"Last Name": "Jorge",'
                        '"E-mail": "marciojorge@email",'
                        '"Phone": "123456789"'
                    '}'
                            ']'
                '}')
        f.seek(0)
        data = json.load(f)

contact_book = ContactBook(data, CONTACTS_PATH)
contact_book.remove()