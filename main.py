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
        self.menu_choices = {('A', 'ADD', '[A]dd contact'): self.add,
                ('R', 'REMOVE', '[R]emove contact'): self.remove,
                ('E', 'EDIT', '[E]dit contact'): self.edit,
                ('S', 'SEE', '[S]ee contacts'): self.see,
                ('U', 'UNDO', '[U]ndo last action'): self.undo,
                ('C', 'CLOSE', '[C]lose the contact book'): close}

    # Adds a contact
    def add(self):
        # Creates the new contact temporarily
        temp_contact = {}
        for info in self.contact_info:
            clear()
            temp_info = input(f'{info}: ')
            temp_contact[info] = temp_info
        clear()

        # Saves the new contact
        confirmation = input('Are you sure you want to create this contact? (Y/N): ').upper()
        if confirmation.startswith('Y'):
            # Deepcopy added to the history
            self.history.append(deepcopy(self.contacts))
            self.contacts['contacts'].append(temp_contact)
            json_contacts = json.dumps(self.contacts)
            with open(self.json_file, 'w+') as f:
                f.truncate(0)
                f.seek(0)
                f.write(json_contacts)
                f.seek(0)
        clear()

    # Removes a contact
    def remove(self):
        # Checks if there are contacts
        clear()
        if not self.contacts['contacts']:
            print('There are no contacts to delete...\n')
            pause()
            clear()
            return

        # Indexes the contacts and then asks the user which one it wants to select
        index = 1
        for contact in self.contacts['contacts']:
            print(f"{index} - {contact['First Name']} {contact['Last Name']}")
            index += 1
        to_delete = input('\nWhich contact would you like to delete? (ID Number): ')
        clear()

        # Deletes the contact
        confirmation = input('Are you sure you want to delete this contact? (Y/N): ').upper()
        if confirmation.startswith('Y'):
            try:
                # Deepcopy added to the history
                self.history.append(deepcopy(self.contacts))
                # Validates selected contact
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
    
    # Edits a contact's information
    def edit(self):
        # Checks if there are contacts to edit
        clear()
        if not self.contacts['contacts']:
            print('There are no contacts to edit...\n')
            pause()
            clear()
            return

        # Indexes the contacts and then asks the user which one it wants to select
        index = 1
        for contact in self.contacts['contacts']:
            print(f"{index} - {contact['First Name']} {contact['Last Name']}")
            index += 1
        to_edit = input('\nWhich contact would you like to edit? (ID Number): ')
        
        # Validates selected index
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

        # Indexes the infos and then asks the user which one it wants to select
        index = 1
        for info in self.contact_info:
            print(f"{index} - {info}")
            index += 1
        to_edit_info = input('\nWhich info would you like to edit? (ID Number): ')

        # Validates the selected info
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
        
        # Asks the user what it wants the info to be edited into
        info_edit = input(f"What would you like the new {new_info} for {contact_edit['First Name']} {contact_edit['Last Name']} to be?: ")
        clear()

        # Edits the contact
        confirmation = input('Are you sure you want to edit this contact? (Y/N): ').upper()
        if confirmation.startswith('Y'):
            # Deepcopy added to the history
            self.history.append(deepcopy(self.contacts))
            contact_edit[new_info] = info_edit
            json_contacts = json.dumps(self.contacts)
            with open(self.json_file, 'w+') as f:
                f.truncate(0)
                f.seek(0)
                f.write(json_contacts)
                f.seek(0)
        clear()

    # Shows a contact's information
    def see(self):
        # Indexes the contacts and then asks the user which one it wants to select
        clear()
        index = 1
        for contact in self.contacts['contacts']:
            print(f"{index} - {contact['First Name']} {contact['Last Name']}")
            index += 1
        to_see = input('\nWhich contact would you like to see? (ID Number): ')

        # Validates the selected contact
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
        
        # Shows contact info
        for key, value in contact_see.items():
            print(f'{key} - {value}')
        print()
        pause()
        clear()

    # Undoes last action
    def undo(self):
        # Checks if there are actions to undo
        clear()
        if not self.history:
            print('There is nothing to undo...\n')
            pause()
            clear()
            return
        
        # Undoes it
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

    # Brings up a menu to use the contact book
    def menu(self):
        clear()
        while True:
            choices_str = ''
            for choice in self.menu_choices.keys():
                choices_str += f'{choice[-1]} | '
            choices_str = choices_str[:-3]
            print(f'What would you like to do with your contact book?\n\n{choices_str}\n')
            choice_selected = input().upper()

            for choice in self.menu_choices.keys():
                if choice_selected in choice:
                    self.menu_choices[choice]()


if __name__ == '__main__':     
    FILE_PATH = Path(__file__).absolute().parent
    CONTACTS_PATH = FILE_PATH / 'contacts.json'

    # Loads contact book data from contacts.json, creates new file if it doesn't exist
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
    contact_book.menu()