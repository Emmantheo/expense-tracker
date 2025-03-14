import pytest
from app import app, expenses
from datetime import datetime
from flask import url_for

@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config["TESTING"] = True  # Enable test mode
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Test if the home page loads successfully."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Expense Tracker" in response.data

def test_set_budget(client):
    """Test setting a monthly budget."""
    response = client.post("/set_budget", data={"budget": "1000"})
    assert response.status_code == 302  # Redirect after setting budget

    # Check if budget was updated
    response = client.get("/")
    assert b"$1000.0" in response.data

def test_add_expense(client):
    """Test adding an expense."""
    response = client.post(
        "/add",
        data={
            "description": "Groceries", 
            "amount": "150",
            "category": "Food",
            "date": datetime.utcnow().strftime("%Y-%m-%d"),
        },
    )
    assert response.status_code == 302  # Redirect after adding an expense

    # Verify expense was added
    response = client.get("/")
    assert b"Groceries" in response.data
    assert b"$150.0" in response.data

def test_delete_expense(client):
    """Test deleting an expense."""
    # Add an expense first
    client.post(
        "/add",
        data={
            "description": "Test Expense",
            "amount": "50",
            "category": "Bills",
            "date": datetime.utcnow().strftime("%Y-%m-%d"),
        },
    )

    # Get the expense ID
    expense_id = expenses[-1]["id"]

    # Delete the expense
    response = client.get(f"/delete/{expense_id}")
    assert response.status_code == 302  # Redirect after deletion

    # Verify expense was removed
    response = client.get("/")
    assert b"Test Expense" not in response.data

def test_download_report(client):
    """Test downloading the monthly report (PDF)."""
    response = client.get("/report")
    assert response.status_code == 200
    assert response.content_type == "application/pdf"
