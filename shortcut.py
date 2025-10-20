#!/usr/bin/env python3

import os
import pathlib

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def print_menu():
    print("\nSymbolic Link Manager")
    print("Input the following numbers corrosponding to your desired command.")
    print("1. Create a symbolic link")
    print("2. Delete a symbolic link")
    print("3. Generate a symbolic link report")
    print("4. Quit")

def create_symlink():
    source_path = input("\nEnter the full path of the file you want to link: ").strip()
    if os.path.isfile(source_path):
        desktop_path = pathlib.Path.home() / 'Desktop'
        link_name = input("Enter the name for the shortcut (symbolic link): ").strip()
        link_path = desktop_path / link_name
        if link_path.exists():
            print("Error: A file or link named " + link_name + " already exists on your Desktop.")
            return
        try:
            os.symlink(source_path, link_path)
            print("Success: Symbolic link created at " + str(link_path))
        except Exception as e:
            print("Error: Could not create symbolic link: " + e)
    else:
        print("Error: The file does not exist. Please check the path and try again.")
        return

def delete_symlink():
    desktop_path = pathlib.Path.home() / 'Desktop'
    link_name = input("\nEnter the name of the symbolic link to delete: ").strip()
    link_path = desktop_path / link_name

    if link_path.exists() & link_path.is_symlink():
        try:
            link_path.unlink()
            print("Success: Symbolic link " + link_name + " deleted from Desktop.")
        except Exception as e:
            print("Error: Could not delete symbolic link: " + e)
    else:
        if not link_path.exists():
            print("Error: The specified link does not exist.")
            return
        if not link_path.is_symlink():
            print("Error: This is not a symbolic link.")
            return

def generate_report():
    home_dir = pathlib.Path.home()
    desktop_path = home_dir / 'Desktop'
    print("\nSymbolic Link Report")

    desktop_links = []
    for item in desktop_path.iterdir():
        if item.is_symlink():
            desktop_links.append(item)

    if len(desktop_links) != 0:
        print("\nSymlinks on Desktop:")
        for link in desktop_links:
            try:
                target = os.readlink(link)
                print("- " + link.name + " -> " + target)
            except Exception as e:
                print("- " + link.name + " -> [Error reading target: [" + str(e) + "]")
    else:
        print("\nNo symbolic links found on Desktop.")

    symlink_count = 0
    for root, dirs, files in os.walk(home_dir):
        for name in dirs + files:
            full_path = os.path.join(root, name)
            if os.path.islink(full_path):
                symlink_count += 1

    print("\nTotal symbolic links in home directory: " + str(symlink_count))

def main():
    while True:
        print_menu()
        choice = input("\nSelect an option [1-4]: ").strip()

        if choice == '1':
            create_symlink()
        elif choice == '2':
            delete_symlink()
        elif choice == '3':
            generate_report()
        elif choice == '4' or choice.lower() == 'quit':
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please enter a number between 1 and 4.")

if __name__ == '__main__':
    main()
    
