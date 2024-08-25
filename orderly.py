#!/usr/bin/env python3
import argparse
from pathlib import Path
import shutil
import yaml
import os
from prettytable import PrettyTable
import stat
import platform
import sys
import random
import string


def check_os():
    try:
        user_os = platform.system()
        if user_os == "Windows":
            return 1
        elif user_os == "Linux":
            return 2
        elif user_os == "Darwin":
            return 3
        else:
            return 4
    except Exception as e:
        print(e)
    
user_os_result = check_os()
if user_os_result == 1:
    try:
        import ctypes# Windows
        import winreg
    except Exception as e:
        print(e)

# Constants
RESET = "\033[0m"

# Foreground Colors
FG_BLACK = "\033[30m"
FG_RED = "\033[31m"
FG_GREEN = "\033[32m"
FG_YELLOW = "\033[33m"
FG_BLUE = "\033[34m"
FG_MAGENTA = "\033[35m"
FG_CYAN = "\033[36m"
FG_WHITE = "\033[37m"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Determine default config file location based on OS
user_os = platform.system()
if user_os == "Windows":
    CONFIG_FILE_LOCATION = os.path.expandvars('%APPDATA%\\Orderly')
    if not os.path.exists(CONFIG_FILE_LOCATION):
        os.makedirs(CONFIG_FILE_LOCATION)
elif user_os in ("Linux", "Darwin"):  # Linux or macOS
    CONFIG_FILE_LOCATION = os.path.expanduser("~/.config/Orderly")
    if not os.path.exists(CONFIG_FILE_LOCATION):
        os.makedirs(CONFIG_FILE_LOCATION)
else:
    CONFIG_FILE_LOCATION = SCRIPT_DIR  # Default to script directory for unsupported OS

CONFIG_FILE = os.path.join(CONFIG_FILE_LOCATION, "course_config.yaml")
CONFIG_FILE_backup = os.path.join(CONFIG_FILE_LOCATION, "conf.bckup.yml")

def clear_screen():
    """
    Clears the terminal screen using ANSI escape codes, which are widely supported.
    """
    
    print("\033[2J\033[H", end="")  # ANSI escape codes to clear screen and move cursor to home position


def show_welcome_message():
    """
    Displays a welcome message to the user.
    """
    try:
        clear_screen()
        table = PrettyTable()
        table.field_names = ["Orderly"]

        # Add rows to the table
        table.add_row([f"{FG_BLUE}Programmer : Pouya Shahrdami! 😊{RESET}"])
        table.add_row([f"{FG_CYAN}-------------------------------------------{RESET}"])
        table.add_row(["Available options:"])
        table.add_row([f"1. {FG_YELLOW}Set up/edit course configuration (creates {CONFIG_FILE}){RESET}"])
        table.add_row([f"2. {FG_YELLOW}Organize files based on existing configuration{RESET}"])
        table.add_row([f"3. {FG_YELLOW}Edit configuration file directly{RESET}"])
        table.add_row([f"4. {FG_YELLOW}Reset configuration (delete {CONFIG_FILE}){RESET}"])
        table.add_row([f"{FG_CYAN}-------------------------------------------{RESET}"])
        table.add_row([f"{FG_MAGENTA}Command-line options:{RESET}"])
        table.add_row([f"{FG_WHITE}--edit{RESET}   Edit the configuration file"])
        table.add_row([f"{FG_WHITE}--reset{RESET}    Delete the existing configuration file"])
        table.add_row([f"{FG_WHITE}--src <directory>{RESET}   Specify a source directory to organize"])
        table.add_row([f"{FG_BLUE}-------------------------------------------{RESET}"])
        table.add_row([f"{FG_WHITE}GitHub: https://github.com/pouyashahrdami{RESET}"])
        table.add_row([f"{FG_BLUE}LinkedIn{FG_WHITE}: https://www.linkedin.com/in/pouya-shahrdami-9aa42b303/{RESET}"])

        print(table)
    except Exception as e:
        print(e)
        


def gather_user_input(base_directory=None):
    try:
        if base_directory is None:
            base_directory = input("Enter the base directory for your folders (leave blank to use the current directory): ").strip()
            if not base_directory:
                base_directory = Path.cwd()
            else:
                base_directory = Path(base_directory)
                if not base_directory.exists():
                    print(f"{FG_RED}The directory '{base_directory}' does not exist.{RESET}")
                    create_directory = input(f"Do you want to create the directory '{base_directory}'? (yes/no): ").strip().lower()
                    if create_directory in ('yes', 'y'):
                        base_directory.mkdir(parents=True, exist_ok=True)
                        print(f"{FG_GREEN}Directory '{base_directory}' created.{RESET}")
                    else:
                        print(f"{FG_RED}Please provide a valid directory path.{RESET}")
                        exit(1)
        else:
            base_directory = Path(base_directory)
        
        show_welcome_message()
        clear_screen()
        
        course_count = int(input("Enter the number of Subjects: "))
        courses = {}
        for i in range(course_count):
            prefix = input(f"Enter prefix for Subject {i+1}: ").strip().lower()
            courses[prefix] = None  # Placeholder for folder path

        # Determine default config file location based on OS
        os_model = check_os()
        if os_model == 1:  # Windows
            config_file_location = CONFIG_FILE_LOCATION
            if not os.path.exists(config_file_location):
                os.makedirs(config_file_location, exist_ok=True)
        elif os_model in (2, 3):  # Linux or macOS
            config_file_location = os.path.expanduser("~/.config/Orderly")  # Adjust as needed
            if not os.path.exists(config_file_location):
                os.makedirs(config_file_location, exist_ok=True)
        else:
            config_file_location = Path.cwd()  # Default to current directory for unsupported OS

        return base_directory, courses, config_file_location

    except ValueError:
        print(f"{FG_RED}Invalid number of courses entered. Please enter an integer.{RESET}")
        exit(1)
    except Exception as e:
        print(f"{FG_RED}Error: {e}{RESET}")
        exit(1)
def save_config(base_directory, courses, config_file_location=CONFIG_FILE_LOCATION):
    try:
        config_data = {
            'base_directory': str(base_directory),
            'courses': courses
        }

        # Construct the full path to the configuration file
        config_file_path = os.path.join(config_file_location, CONFIG_FILE)

        with open(config_file_path, 'w') as file:
            yaml.dump(config_data, file)

        os_model = check_os()

        if os_model == 1:
            CONFIG_FILE_backup = os.path.join(config_file_location, "conf.bckup.yml")
            with open(CONFIG_FILE_backup, 'w') as file:
                yaml.dump(config_data, file)
            os.system(f'attrib +h "{CONFIG_FILE_backup}"')
        elif os_model == 2 or 3:
            CONFIG_FILE_backup = os.path.join(config_file_location, ".conf.bckup.yml")
            with open(CONFIG_FILE_backup, 'w') as file:
                yaml.dump(config_data, file)
        else:
            print("Just creating the file, no backup needed.")

        os.chmod(config_file_path, stat.S_IRUSR)
        print(f"{FG_GREEN}Configuration saved to {config_file_path}. Please run the application again.{RESET}")

    except Exception as e:
        print(f"{FG_RED}Error saving configuration: {e}{RESET}")

def load_config(config_file_location=CONFIG_FILE_LOCATION):
    try:
        config_file_path = os.path.join(config_file_location, CONFIG_FILE)
        if Path(config_file_path).exists():
            with open(config_file_path, 'r') as file:
                return yaml.load(file, Loader=yaml.FullLoader)

        config_backup_path = os.path.join(config_file_location, CONFIG_FILE_backup)
        if Path(config_backup_path).exists():
            is_back_up = input("Your main config file is missing or corrupted. Do you want to use the backup? (yes/no): ").strip().lower()
            if is_back_up.lower() in ('yes', 'y'):
                with open(config_backup_path, 'r') as file:
                    return yaml.load(file, Loader=yaml.FullLoader)
            else:
                print("You can use '--reset' to reset your config file.")
        else:
            print("No configuration or backup file found.")
            show_welcome_message()
        return None
    except Exception as e:
        print(f"{FG_RED}Error loading configuration: {e}{RESET}")
        return None

def locate_or_create_folders(base_directory, courses):
    for prefix in courses.keys():
        try:
            folder_name = input(f"Enter folder name for prefix '{prefix}': ").strip()
            folder_path = base_directory / folder_name

            if folder_path.exists():
                print(f"{FG_YELLOW}Folder '{folder_name}' already exists. Skipping creation...{RESET}")
            courses[prefix] = str(folder_path)
        except Exception as e:
            print(f"{FG_RED}Error: {e}{RESET}")

def find_folders(courses, directory):
    matching_folders = []
    try:
        print(f"{FG_CYAN}Searching in directory: {directory}{RESET}")
        for item in directory.iterdir():
            if item.is_dir():
                item_name_lower = item.name.lower()
                for prefix, destination_folder in courses.items():
                    if item_name_lower.startswith(prefix):
                        destination_folder_path = Path(destination_folder)
                        matching_folders.append(item)

                        new_path = destination_folder_path / item.name
                        
                        if new_path.exists():
                                print(f"{FG_YELLOW}Folder {item} already exists in the destination.{RESET}")
                                user_input = input("Do you want to overwrite this folder? (y/n): ").strip().lower()

                                if user_input == 'y':
                                    shutil.move(item, new_path)
                                    print(f"{FG_GREEN}Moved {item} to {new_path} (overwritten){RESET}")
                                else:
                                    print(f"{FG_GREEN}Skipped folder: {item}{RESET}")
                        else:
                            shutil.move(item, new_path)
                            print(f"{FG_GREEN}Moved {item} to {new_path}{RESET}")
                        break
    except Exception as e:
        print(f"{FG_RED}An error occurred: {e}{RESET}")
    
    return matching_folders


def parse_arguments():
    parser = argparse.ArgumentParser(description="Course Folder Management Application")
    parser.add_argument('--edit', action='store_true', help="Edit the configuration file")
    parser.add_argument('--reset', action='store_true', help="Delete the configuration file")
    parser.add_argument('--src', type=str, help="Specify a source directory to organize (default is the current directory)")

    return parser.parse_args()

def elevate_privileges():
    """Attempts to elevate privileges, prompting the user if necessary."""
    os_model = check_os()
    if os_model == 1:  # Windows
        # Using ctypes to trigger UAC prompt
        if ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1) <= 32:
            print(f"{FG_RED}Error: Unable to elevate privileges. Exiting.{RESET}")
            sys.exit(1)
    elif os_model in (2, 3):  # Linux/macOS
        # Using 'sudo' to request elevation
        print(f"{FG_YELLOW}This operation requires root privileges. You will be prompted for your password.{RESET}")
        os.execvp("sudo", ["sudo"] + sys.argv)
        
def is_admin():
    """Checks if the script is running with administrator/root privileges."""
    try:
        os_model = check_os()  # Assuming you have this function
        if os_model == 1:  # Windows
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        elif os_model in (2, 3):  # Linux/macOS
            return os.getuid() == 0
    except Exception:
        return False
    
def main():
    args = parse_arguments()

    try:
        if args.edit:
            try:
                if not Path(CONFIG_FILE).exists():
                    print(f"{FG_RED}Configuration file not found: {CONFIG_FILE}{RESET}")
                    return
                # Open the configuration file in the user's default editor
                if user_os_result == 1:  # Windows
                    os.startfile(CONFIG_FILE)
                elif user_os_result in (2, 3):  # Linux or macOS
                    editor = os.getenv('EDITOR', 'nano')  # Default to nano if $EDITOR isn't set
                    os.system(f'{editor} {CONFIG_FILE}')
                else:
                    print(f"{FG_RED}Unsupported OS for editing the configuration file.{RESET}")
            except Exception as e:
                print(f"{FG_RED}Error while trying to open the configuration file: {e}{RESET}")
            return
        # Handle reset option
        if args.reset:
            try:
                clear_screen()
                if not is_admin():
                    elevate_privileges()

                # Get the default config location to delete the file and backup
                os_model = check_os()
                if os_model == 1:
                    default_config_location = CONFIG_FILE_LOCATION
                elif os_model in (2, 3):
                    default_config_location = "~/.config/Orderly"
                else:
                    default_config_location = Path.cwd()

                config_file_path = os.path.join(default_config_location, CONFIG_FILE)
                config_backup_path = os.path.join(default_config_location, CONFIG_FILE_backup)

                # Delete the configuration and backup files if they exist
                if Path(config_file_path).exists():
                    os.remove(config_file_path)
                    print(f"{FG_GREEN}Configuration file '{CONFIG_FILE}' deleted.{RESET}")
                else:
                    print(f"{FG_YELLOW}No configuration file found to delete.{RESET}")
                
                if Path(config_backup_path).exists():
                    os.remove(config_backup_path)
                    print(f"{FG_GREEN}Configuration backup file '{CONFIG_FILE_backup}' deleted.{RESET}")
                else:
                    print(f"{FG_YELLOW}No backup configuration file found to delete.{RESET}")
                
            except Exception as e:
                print(f"{FG_RED}Error deleting configuration file: {e}{RESET}")
                print(f'Please delete the config file manually. File location: {CONFIG_FILE_LOCATION}')
            
            exit(0)  # Exit after resetting

        # Load configuration file
        config_file_location = CONFIG_FILE_LOCATION
        config = load_config(config_file_location) if not args.reset else None

        # Get base directory from config or gather user input
        if config:
            base_directory = Path(config.get('base_directory', Path.cwd()))
        else:
            base_directory, courses, config_file_location = gather_user_input()

        # Organizing with a source directory or current directory
        if args.src:  # If the --src option is provided
            directory_to_organize = Path(args.src)
            if not directory_to_organize.exists():
                print(f"{FG_RED}The source directory '{directory_to_organize}' does not exist.{RESET}")
                exit(1)
        else:  # Use the current working directory if no --src option is provided
            directory_to_organize = Path.cwd()

        # Locate and create folders based on user input
        if  not config:
            try:
                if not config:
                    # If no config exists, gather user input for base directory and courses
                    base_directory, courses, config_file_location = gather_user_input()
                else:
                    # but prompt user for new folder names
                    courses = config['courses']  
                    base_directory = Path(config.get('base_directory', Path.cwd()))

                # Locate or create folders (will now always have 'courses' defined)
                locate_or_create_folders(base_directory, courses)

                # Save the updated configuration
                save_config(base_directory, courses, config_file_location)

                # Organize files based on the (potentially updated) folders
                matching_folders = find_folders(courses, directory_to_organize)
                if not matching_folders:
                    print(f"{FG_YELLOW}No matching folders found.{RESET}")

            except Exception as e:
                print(f"{FG_RED}Error while creating folders or saving configuration: {e}{RESET}")
                exit(1)
                
        # Handle organization based on existing config
        if config:
            try:
                matching_folders = find_folders(config['courses'], directory_to_organize)
                if not matching_folders:
                    print(f"{FG_YELLOW}No matching folders found.{RESET}")

            except Exception as e:
                print(f"{FG_RED}An error occurred while finding folders: {e}{RESET}")
                exit(1)

    except Exception as e:
        print(f"{FG_RED}An unexpected error occurred: {e}{RESET}")
        exit(1)



if __name__ == "__main__":

    main()
