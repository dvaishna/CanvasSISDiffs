import os
import csv
import re

def get_directories_with_csv_files(parent_directory):
    """
    Recursively searches for directories containing errors.csv, enrolment.csv, and sections.csv.
    """
    directories = []
    for root, dirs, files in os.walk(parent_directory):
        if 'errors.csv' in files and 'enrollments.csv' in files and 'sections.csv' in files:
            directories.append(root)
    return directories

def compare_timestamps_and_messages(directories):
    """
    Compares the timestamps of directories and extracts newly added messages from errors.csv.
    """
    directories.sort(key=os.path.getmtime)  # Sort directories based on creation time
    old_dir = directories[0]
    new_dir = directories[-1]

    old_errors_csv = os.path.join(old_dir, 'errors.csv')
    new_errors_csv = os.path.join(new_dir, 'errors.csv')

    old_messages = set()
    new_messages = set()

    with open(old_errors_csv, 'r') as file:
        csv_reader = csv.DictReader(file)
        old_messages = {row['message'] for row in csv_reader}

    with open(new_errors_csv, 'r') as file:
        csv_reader = csv.DictReader(file)
        new_messages = {row['message'] for row in csv_reader}

    newly_added_messages = new_messages - old_messages

    return newly_added_messages


def extract_section_numbers_and_check_status(message, errors_csv_directory):
    """
    Extracts the section number from the error message.
    """
    pattern = r'section (\S+)'
    match = re.search(pattern, message)
    if match:
        section_number = match.group(1)
        enrolment_csv_path = os.path.join(errors_csv_directory, 'enrollments.csv')
        with open(enrolment_csv_path, 'r') as enrolment_file:
            csv_reader = csv.DictReader(enrolment_file)
            for row in csv_reader:
                if row['section_id'] == section_number:
                    if row['status'] == 'active':
                        print(f"Active section found for which An enrollment referenced a non-existent section: {section_number}")
                    break

if __name__ == "__main__":
    parent_directory = "C:\Python_Proj\sis-canvas"

    directories = get_directories_with_csv_files(parent_directory)

    if len(directories) < 2:
        print("At least two directories with errors.csv, enrolment.csv, and sections.csv are needed for comparison.")
    else:
        newly_added_messages = compare_timestamps_and_messages(directories)

        print("Newly added messages in the latest timestamped directory: ")
        for message in newly_added_messages:
            extract_section_numbers_and_check_status(message, directories[-1])