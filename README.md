**What it does:**

This Python script automates the process of identifying newly added error messages in a Student Information System (SIS) and Canvas Learning Management System (LMS) integration. It helps detect potential enrollment errors related to non-existent sections.

**How it works:**

1. Directory Discovery:
    - The script searches a specified directory structure for subdirectories containing three required CSV files:
      - errors.csv
      - enrollments.csv
      - sections.csv
2. Error Message Comparison:
    - It compares the timestamps of these directories and focuses on the one with the latest modification time (assumed to be the most recent).
    - The script then compares the 'message' field in errors.csv files from the newest directory with a previous version (determined by timestamp).
    - This comparison identifies newly added error messages.
3. Error Validation and Reporting:
    - For each newly added message, the script attempts to extract a section number.
    - If a section number is found, it checks the enrollments.csv file within the latest directory for a matching 'section_id'.
    - If a matching enrollment record exists and its status is 'active', the script prints an error message indicating a potential discrepancy: an active enrollment referencing a potentially non-existent section.

**How to use it:**

1. Update the parent_directory variable at the bottom of the script to point to the root directory containing the subdirectories with the required CSV files.
2. Run the script using: python sis_canvas_error_checker.py

**Notes:**
  - This script assumes a specific directory structure and CSV file format. Anpassments might be necessary for different configurations.
  - Error handling is not explicitly implemented. Consider adding checks for potential file access or parsing errors.
