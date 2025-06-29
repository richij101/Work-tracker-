# Simple Time Tracker

A web-based application to track worked days (by location), vacation days, and travel days.

## Features

*   Input dates using a calendar date picker (single day or range).
*   Categorize entries as "Work", "Vacation", or "Traveling".
*   Specify location for "Work" entries.
*   View summaries:
    *   Total worked days
    *   Total vacation days
    *   Total travel days
    *   Breakdown of worked days by location.
*   View a log of all entries.

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
    The application will start the Flask development server. By default, it should be accessible at `http://127.0.0.1:5000/` in your web browser. The first time you run it, an `instance` folder containing `time_tracker.db` will be created.

## How to Use

1.  Open the application in your web browser (usually `http://127.0.0.1:5000/`).
2.  Use the form to add new entries:
    *   Select a **Start Date**.
    *   Optionally, select an **End Date** if logging a range of days. If not selected, it defaults to the Start Date.
    *   Choose the **Type** of entry: "Work Land", "Work Ship", "Vacation", or "Traveling".
    *   If "Work Land" is selected, a "Country" field will appear. Select or type to filter and choose a country. This field is required.
    *   If "Work Ship" is selected, a "Ship Name" field will appear. Enter the name of the ship. This field is required.
    *   The "Country" and "Ship Name" fields are hidden for "Vacation" and "Traveling" types.
    *   Click "Add Entry".
3.  View the updated summaries and the log of all entries on the page. The "Location" column in summaries and logs will show the Country for "Work Land" entries or the Ship Name for "Work Ship" entries.

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