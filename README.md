
## Orderly - Course Folder Management Application

<img src="orderly.jpeg" alt="orderly" width="100%" height="450">

Orderly is a command-line tool to help you create, organize, and move folders based on course prefixes, making it easy to keep your course materials tidy.

## Features

- **Set up a base directory:** Choose a central location for all your course folders.
- **Create and organize folders:** Define course prefixes and let Orderly create folders for you.
- **Move folders to designated locations:** Easily move existing folders to their proper places based on course prefixes.
- **Customizable:** Use command-line options to change the default directory and reset your configuration.

## Installation

1. Clone this repository: `git clone https://github.com/pouyashahrdami/orderly.git`
2. Navigate to the project directory: `cd Orderly`
3. Make the script executable (Linux/macOS): `chmod +x Orderly.py`

## Usage

Bash

  

```
python Orderly.py [options]
```

  

### Options

- `--edit`: Edit the configuration file in your default text editor.
- `--reset`: Delete the existing configuration file and start fresh.
- `--src <directory>`: Specify a source directory to organize (default is the current directory).

### First-Time Setup

1. Run `python Orderly.py`. You will be prompted to:
    - Enter the base directory for your course folders.
    - Enter the number of courses you have.
    - Enter the prefix for each course.
    - Enter the desired folder name for each course prefix.
2. Orderly will create the necessary folders in your base directory and save the configuration.

### Subsequent Runs

- Run `python Orderly.py` to organize folders in your current directory based on your saved configuration.
- Use `--src <directory>` to organize a specific directory.
- Use `--edit` to modify your course prefixes or folder names.
- Use `--reset` to delete your configuration and start over.

## Configuration File

Orderly stores your base directory and course prefixes in a configuration file. The default location is:

- Windows: `%APPDATA%\Orderly\course_config.yaml`
- Linux/macOS: `~/.config/Orderly/course_config.yaml`

## Contributing

Feel free to submit pull requests or open issues to help improve Orderly!