"""

This program is a contact book through the terminal

"""

from pathlib import Path
from copy import deepcopy
import json
import os
import sys

def clear():
    return os.system('cls')

def pause():
    return os.system('pause')

def close():
    clear()
    return sys.exit()

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

        confirmation = input('Are you sure you want to delete this contact? (Y/N): ').upper()
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
    
    def edit(self):
        clear()
        if not self.contacts['contacts']:
            print('There are no contacts to edit...\n')
            pause()
            clear()
            return

        index = 1
        for contact in self.contacts['contacts']:
            print(f"{index} - {contact['First Name']} {contact['Last Name']}")
            index += 1
        to_edit = input('\nWhich contact would you like to edit? (ID Number): ')
        
        try:
            to_edit = int(to_edit)
            if to_edit <= 0:
                raise ValueError('Index has to be bigger than 0')
            to_edit -= 1
            contact_edit = self.contacts['contacts'][to_edit]
            clear()
        except(ValueError, IndexError):
            clear()
            print('Invalid contact ID...\n')
            pause()
            clear()
            return

        index = 1
        for info in self.contact_info:
            print(f"{index} - {info}")
            index += 1
        to_edit_info = input('\nWhich info would you like to edit? (ID Number): ')

        try:
            to_edit_info = int(to_edit_info)
            if to_edit_info <= 0:
                raise ValueError('Index has to be bigger than 0')
            to_edit_info -= 1
            new_info = self.contact_info[to_edit_info]
            clear()
        except(ValueError, IndexError):
            clear()
            print('Invalid info ID...\n')
            pause()
            clear()
            return
        
        info_edit = input(f"What would you like the new {new_info} for {contact_edit['First Name']} {contact_edit['Last Name']} to be?: ")
        clear()

        confirmation = input('Are you sure you want to edit this contact? (Y/N): ').upper()
        if confirmation.startswith('Y'):
            self.history.append(deepcopy(self.contacts))
            contact_edit[new_info] = info_edit
            json_contacts = json.dumps(self.contacts)
            with open(self.json_file, 'w+') as f:
                f.truncate(0)
                f.seek(0)
                f.write(json_contacts)
                f.seek(0)
        clear()

    def see(self):
        clear()
        index = 1
        for contact in self.contacts['contacts']:
            print(f"{index} - {contact['First Name']} {contact['Last Name']}")
            index += 1
        to_see = input('\nWhich contact would you like to see? (ID Number): ')

        try:
            to_see = int(to_see)
            if to_see <= 0:
                raise ValueError('Index has to be bigger than 0')
            to_see -= 1
            contact_see = self.contacts['contacts'][to_see]
            clear()
        except(ValueError, IndexError):
            clear()
            print('Invalid contact ID...\n')
            pause()
            clear()
            return
        
        for key, value in contact_see.items():
            print(f'{key} - {value}')
        print()
        pause()
        clear()

    def undo(self):
        clear()
        if not self.history:
            print('There is nothing to undo...\n')
            pause()
            clear()
            return
        
        confirmation = input('Are you sure you want to undo last action? (Y/N): ').upper()
        if confirmation.startswith('Y'):
            clear()
            self.contacts = self.history.pop()
            json_contacts = json.dumps(self.contacts)
            with open(self.json_file, 'w+') as f:
                f.truncate(0)
                f.seek(0)
                f.write(json_contacts)
                f.seek(0)
            
            print('Last action undone\n')
            pause()
        clear()

def cb_menu(contact_book: ContactBook):
    choices = {('A', 'ADD', '[A]dd contact'): contact_book.add,
               ('R', 'REMOVE', '[R]emove contact'): contact_book.remove,
               ('E', 'EDIT', '[E]dit contact'): contact_book.edit,
               ('S', 'SEE', '[S]ee contacts'): contact_book.see,
               ('U', 'UNDO', '[U]ndo last action'): contact_book.undo,
               ('C', 'CLOSE', '[C]lose the contact book'): close}
    while True:
        choices_str = ''
        for choice in choices.keys():
            choices_str += f'{choice[-1]} | '
        choices_str = choices_str[:-3]
        print(f'What would you like to do with your contact book?\n\n{choices_str}\n')
        choice_selected = input().upper()

        for choice in choices.keys():
            if choice_selected in choice:
                choices[choice]()


if __name__ == '__main__':     
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
                            '"E-mail": "example@email.com",'
                            '"Phone": "1234-5678"'
                        '}'
                                ']'
                    '}')
            f.seek(0)
            data = json.load(f)

    contact_book = ContactBook(data, CONTACTS_PATH)
    cb_menu(contact_book)