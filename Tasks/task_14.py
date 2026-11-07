''' Task 14 | Command-Line Contact Manager
Concepts: Modules, JSON, CRUD, validation
Problem: Build a menu-driven CLI contact manager with add, search, update, delete, list, and persistent JSON storage. Each contact has a unique ID, name, phone, and email.
Requirements: Use separate functions/modules for storage and business logic. Handle missing/corrupt JSON safely without silently deleting existing data. Search names case-insensitively.
Sample / expected behavior: Add ID=1, name="Ayesha"; restart application; search "aye" -> contact remains available.'''


import json
import os


FILE_NAME = "contacts.json"




def load_contacts():
    """Load contacts from JSON file."""

    if not os.path.exists(FILE_NAME):
        save_contacts([])
        return []

    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            contacts = json.load(file)

        if not isinstance(contacts, list):
            raise ValueError("Contact file must contain a list")

        for contact in contacts:
            if not isinstance(contact, dict):
                raise ValueError("Invalid contact data")

            if not all(
                field in contact
                for field in ("contact_id", "name", "phone", "email")
            ):
                raise ValueError("Contact is missing required fields")

        return contacts

    except json.JSONDecodeError:
        raise ValueError("Contacts file contains invalid JSON")


def save_contacts(contacts):
    """Save contacts safely to JSON file."""

    temporary_file = FILE_NAME + ".tmp"

    with open(temporary_file, "w", encoding="utf-8") as file:
        json.dump(contacts, file, indent=4)

    os.replace(temporary_file, FILE_NAME)




def add_contact(contacts):
    print("\nADD CONTACT")
    print("-" * 40)

    contact_id = input("Enter Contact ID: ").strip()

    if not contact_id:
        print("Contact ID cannot be empty")
        return

    if any(contact["contact_id"] == contact_id for contact in contacts):
        print("Contact ID already exists")
        return

    name = input("Enter Name: ").strip()
    phone = input("Enter Phone: ").strip()
    email = input("Enter Email: ").strip()

    if not name or not phone or not email:
        print("All fields are required")
        return

    if "@" not in email:
        print("Invalid email address")
        return

    contact = {
        "contact_id": contact_id,
        "name": name,
        "phone": phone,
        "email": email
    }

    contacts.append(contact)
    save_contacts(contacts)

    print("Contact added successfully!")


def search_contact(contacts):
    print("\nSEARCH CONTACT")
    print("-" * 40)

    search_term = input("Enter name, phone, email, or ID: ").strip().lower()

    if not search_term:
        print("Search value cannot be empty")
        return

    found = []

    for contact in contacts:
        if any(
            search_term in str(contact[field]).lower()
            for field in ("contact_id", "name", "phone", "email")
        ):
            found.append(contact)

    if found:
        for contact in found:
            print(contact)
    else:
        print("No contact found")


def update_contact(contacts):
    print("\nUPDATE CONTACT")
    print("-" * 40)

    contact_id = input("Enter Contact ID to update: ").strip()

    for contact in contacts:
        if contact["contact_id"] == contact_id:

            print("Leave a field blank to keep its current value.")

            name = input("Enter new name: ").strip()
            phone = input("Enter new phone: ").strip()
            email = input("Enter new email: ").strip()

            if email and "@" not in email:
                print("Invalid email address")
                return

            if name:
                contact["name"] = name

            if phone:
                contact["phone"] = phone

            if email:
                contact["email"] = email

            save_contacts(contacts)

            print("Contact updated successfully!")
            return

    print("Contact not found")


def delete_contact(contacts):
    print("\nDELETE CONTACT")
    print("-" * 40)

    contact_id = input("Enter Contact ID to delete: ").strip()

    for contact in contacts:
        if contact["contact_id"] == contact_id:
            contacts.remove(contact)
            save_contacts(contacts)

            print("Contact deleted successfully!")
            return

    print("Contact not found")


def list_contacts(contacts):
    print("\nALL CONTACTS")
    print("-" * 40)

    if not contacts:
        print("No contacts available")
        return

    for contact in contacts:
        print("ID:", contact["contact_id"])
        print("Name:", contact["name"])
        print("Phone:", contact["phone"])
        print("Email:", contact["email"])
        print("-" * 40)



def main():
    try:
        contacts = load_contacts()
    except (ValueError, OSError) as error:
        print("Unable to load contacts:", error)
        print("Please repair the JSON file before continuing.")
        return

    while True:
        print("\nCONTACT MANAGEMENT SYSTEM")
        print("=" * 40)
        print("1. Add Contact")
        print("2. Search Contact")
        print("3. Update Contact")
        print("4. Delete Contact")
        print("5. List All Contacts")
        print("6. Exit")
        print("=" * 40)

        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            add_contact(contacts)

        elif choice == "2":
            search_contact(contacts)

        elif choice == "3":
            update_contact(contacts)

        elif choice == "4":
            delete_contact(contacts)

        elif choice == "5":
            list_contacts(contacts)

        elif choice == "6":
            print("Thank you for using Contact Manager!")
            break

        else:
            print("Invalid choice. Please select 1 to 6.")



if __name__ == "__main__":
    main()
