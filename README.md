# Simple Time Tracker

A web-based application to track worked days (by location), vacation days, and travel days.

## Features

*   Input date ranges (or single days) which are stored as single entries.
*   Categorize entries as "Work Land" (with Country), "Work Ship" (with Ship Name), "Vacation", or "Traveling".
*   Country input for "Work Land" is a filterable dropdown.
*   View summaries:
    *   Total worked days (calculated from date ranges).
    *   Total vacation days (calculated from date ranges).
    *   Total travel days (calculated from date ranges).
    *   Breakdown of worked days by location (Country or Ship Name).
*   View a log of all entries, showing date ranges.
*   Edit existing entries.
*   Delete existing entries (with confirmation).

## Technology Stack

*   **Backend:** Python, Flask
*   **Database:** SQLite
*   **Frontend:** HTML, CSS, JavaScript (with Flatpickr.js for date selection)

## Setup and Installation

1.  **Clone the repository (or download the files):**
    ```bash
    # git clone <repository_url> # If it were a git repo
    # cd <repository_directory>
    ```
    (Assuming you have the files in a directory)

2.  **Create a Python virtual environment (recommended):**
    ```bash
    python3 -m venv venv  # Or python -m venv venv
    ```

3.  **Activate the virtual environment:**
    *   On macOS and Linux:
        ```bash
        source venv/bin/activate
        ```
    *   On Windows:
        ```bash
        venv\\Scripts\\activate
        ```

4.  **Install dependencies:**
    Make sure you are in the project root directory where `requirements.txt` is located.
    ```bash
    pip install -r requirements.txt
    ```

5.  **Run the application:**
    ```bash
    python run.py
    ```
    The application will start the Flask development server.
    By default (due to `host='0.0.0.0'`), it will be accessible at `http://127.0.0.1:5000/` and also via the machine's local network IP address (e.g., `http://<your_machine_ip>:5000/`).
    The first time you run it (after deleting any old `time_tracker.db`), an `instance` folder containing the new `time_tracker.db` will be created.
    **Important:** If you are updating from a version prior to range-based entries and edit/delete functionality, you **must delete** the old `instance/time_tracker.db` file before running the application to ensure the new database schema is applied.

## How to Use

1.  Open the application in your web browser (e.g., `http://127.0.0.1:5000/` or `http://<your_machine_ip>:5000/`).
2.  **Adding Entries:**
    *   Use the form to add new entries.
    *   Select a **Start Date** and an **End Date**. For a single day, select the same date for both, or leave End Date blank (it will default to Start Date).
    *   Choose the **Type** of entry: "Work Land", "Work Ship", "Vacation", or "Traveling".
    *   If "Work Land" is selected, a "Country" field will appear. Select or type to filter and choose a country. This field is required.
    *   If "Work Ship" is selected, a "Ship Name" field will appear. Enter the name of the ship. This field is required.
    *   Click "Add Entry". Each submission creates a single entry, even for date ranges.
3.  **Viewing Entries:**
    *   The log displays entries with their date ranges.
    *   Summaries calculate total days based on the duration of these entered ranges.
    *   The "Location" column in summaries and logs will show the Country for "Work Land" entries or the Ship Name for "Work Ship" entries.
4.  **Editing Entries:**
    *   Click the "Edit" button next to an entry in the log.
    *   You will be taken to an edit page with the entry's details pre-filled.
    *   Modify the details as needed and click "Save Changes".
5.  **Deleting Entries:**
    *   Click the "Delete" button next to an entry in the log.
    *   A confirmation dialog will appear. Click "OK" to delete the entry.

## Project Structure

```
.
├── app/
│   ├── __init__.py       # Initializes Flask app, database
│   ├── models.py         # SQLAlchemy database models
│   ├── routes.py         # Flask routes and view logic
│   ├── static/           # (Currently empty, for CSS/JS files if not using CDN)
│   └── templates/
│       └── index.html    # Main HTML template
├── instance/             # (Created automatically by Flask in the project root)
│   └── time_tracker.db   # SQLite database file
├── requirements.txt      # Python package dependencies
├── run.py                # Script to run the Flask application
└── README.md             # This file
```
(Note: The `instance/` directory and `time_tracker.db` file will be created in the project's root directory alongside `run.py` when you first run the application, due to the way `app.instance_path` is used.)