# Expense Tracker

A simple Flask application that allows users to add, view, and delete expenses, set a monthly budget, and generate a monthly expense report in PDF format.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Endpoints](#endpoints)
- [File Structure](#file-structure)
- [Possible Improvements](#possible-improvements)

---

## Features

1. **Add and Delete Expenses**: Users can add new expenses (with date, description, amount, and category) and delete existing ones.
2. **Monthly Budget**: Users can set a monthly budget. The home page shows total spent and remaining budget for the current month.
3. **Expense Categorization**: Predefined categories include Food, Transport, Shopping, Bills, Entertainment, and Other.
4. **PDF Reporting**: A monthly PDF report (for the current month) can be generated, showing a summary of expenses.

---

## Prerequisites

- Python 3.7+ (though any modern version of Python 3 should work)
- [pip](https://pip.pypa.io/en/stable/) for Python package management

---

## Installation

1. **Clone or Download** the repository:

   ```bash
   git clone https://github.com/username/expense-tracker-flask.git
   cd expense-tracker-flask
   ```
2. **Install Dependencies**

To install all necessary dependencies, run:

```bash
pip install -r requirements.txt
```
The primary libraries needed are:

- Flask (for the web framework)

- ReportLab (for PDF generation)
3. (Optional) Create a Virtual Environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage
1. Start the Flask Server:

```bash
python app.py
```

The application will run by default on http://0.0.0.0:5000 (or http://localhost:5000).

2. Open the App:

In your web browser, navigate to:

```arduino
http://localhost:5000
```

You should see the home page with an option to set your monthly budget, view expenses, and add new ones.

3. Add a New Expense:

- Fill out the Description, Amount, Category, and optional Date (defaults to today if empty).

- Click Add Expense.

- You’ll be redirected to the home page with the updated expense list.

4. Delete an Expense:

- Click the Delete link next to an expense entry to remove it from the current list.

5. Generate a PDF Report:

- Click Generate Report (PDF) at the top (or navigate to /report).

- A PDF file will be generated for the current month’s expenses and downloaded automatically.

  ## Endpoints

| Endpoint              | Method | Description                                                           |
|-----------------------|--------|-----------------------------------------------------------------------|
| `/`                   | GET    | Displays the home page with the current month’s expenses.            |
| `/set_budget`         | POST   | Sets the monthly budget.                                              |
| `/add`                | POST   | Adds a new expense (parameters: `description`, `amount`, `category`). |
| `/delete/<int:id>`    | GET    | Deletes the specified expense by ID.                                  |
| `/report`             | GET    | Generates and returns a PDF for the current month’s expenses.         |


## File Structure
```bash
.
├─ app.py               # Main Flask application
├─ templates
│   └─ index.html       # Front-end template for the home page
├─ requirements.txt     # Python dependencies
├─ README.md            # This README file
└─ (other files)        # Additional scripts or assets as needed
```
## Possible Improvements
- Database Integration: Currently, expenses are stored in-memory, so they reset on server restart. Integrating a database (e.g., SQLite, PostgreSQL, MySQL) would provide persistence.

- Authentication: Add user login to make the budget and expenses user-specific.

- More Reporting Options: Provide weekly/yearly PDF reports or CSV/Excel exports.

- Enhanced UI: Improve the front-end design with a modern UI framework like Bootstrap.

- Testing: Implement unit tests or integration tests for endpoints.
