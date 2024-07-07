"""

This program is a contact book through the terminal

"""

from pathlib import Path
from copy import deepcopy
import json
import os

def clear():
    return os.system('cls')

def pause():
    return os.system('pause')

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

        confirmation = input('Are you sure you want to create this contact? (Y/N): ').upper()
        if confirmation.startswith('Y'):
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
        if not self.contacts['contacts']:
            print('There are no contacts to delete...\n')
            pause()
            clear()
            return

        index = 1
        for contact in self.contacts['contacts']:
            print(f"{index} - {contact['First Name']} {contact['Last Name']}")
            index += 1
        to_delete = input('\nWhich contact would you like to delete? (ID Number): ')
        clear()

        confirmation = input('Are you sure you want to delete this contact?(Y/N): ').upper()
        if confirmation.startswith('Y'):
            try:
                self.history.append(deepcopy(self.contacts))
                to_delete = int(to_delete)
                if to_delete <= 0:
                    raise ValueError('Index has to be bigger than 0')
                to_delete -= 1
                self.contacts['contacts'].pop(to_delete)
                json_contacts = json.dumps(self.contacts)
                with open(self.json_file, 'w+') as f:
                    f.truncate(0)
                    f.seek(0)
                    f.write(json_contacts)
                    f.seek(0)
            except(ValueError, IndexError):
                self.history.pop()
                clear()
                print('Invalid contact ID...\n')
                pause()
        clear()
    
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
                        '"First Name": "Example",'
                        '"Last Name": "Example",'
                        '"E-mail": "exemple@email",'
                        '"Phone": "123456789"'
                    '}'
                            ']'
                '}')
        f.seek(0)
        data = json.load(f)

contact_book = ContactBook(data, CONTACTS_PATH)
contact_book.remove()