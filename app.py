import io
from flask import Flask, render_template, request, redirect, send_file
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)

# In-memory list to store expenses
expenses = []
monthly_budget = 0  # Default budget is 0

# Predefined categories
CATEGORIES = ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Other"]

@app.route("/", methods=["GET"])
def home():
    """Display all expenses, total spent, and budget tracking."""
    global monthly_budget

    # Get current month and year
    current_month = datetime.now().strftime("%Y-%m")

    # Filter expenses for the current month
    current_month_expenses = [
        exp for exp in expenses if exp["date"].startswith(current_month)
    ]

    total_spent = sum(exp["amount"] for exp in current_month_expenses)
    remaining_budget = monthly_budget - total_spent if monthly_budget > 0 else 0
    over_budget = total_spent > monthly_budget if monthly_budget > 0 else False

    return render_template(
        "index.html",
        expenses=current_month_expenses,
        total_spent=total_spent,
        remaining_budget=remaining_budget,
        over_budget=over_budget,
        categories=CATEGORIES,
        monthly_budget=monthly_budget,
    )

@app.route("/set_budget", methods=["POST"])
def set_budget():
    """Set the monthly budget."""
    global monthly_budget
    budget = request.form.get("budget")
    if budget:
        monthly_budget = float(budget)
    return redirect("/")

@app.route("/add", methods=["POST"])
def add_expense():
    """Handle adding a new expense."""
    description = request.form["description"]
    amount = request.form["amount"]
    category = request.form["category"]
    date = request.form["date"]

    if not date:
        date = datetime.utcnow().strftime("%Y-%m-%d")

    if description and amount and category:
        new_expense = {
            "id": len(expenses) + 1,  # Assign a unique ID
            "description": description,
            "amount": float(amount),
            "category": category,
            "date": date
        }
        expenses.append(new_expense)

    return redirect("/")

@app.route("/delete/<int:expense_id>", methods=["GET"])
def delete_expense(expense_id):
    """Delete an expense by ID."""
    global expenses
    expenses = [exp for exp in expenses if exp["id"] != expense_id]
    return redirect("/")

@app.route("/report", methods=["GET"])
def generate_report():
    """Generate and download a monthly expense report as a PDF."""
    global monthly_budget

    # Get current month and year
    current_month = datetime.now().strftime("%Y-%m")
    current_month_display = datetime.now().strftime("%B %Y")

    # Filter expenses for the current month
    current_month_expenses = [
        exp for exp in expenses if exp["date"].startswith(current_month)
    ]

    total_spent = sum(exp["amount"] for exp in current_month_expenses)
    remaining_budget = monthly_budget - total_spent if monthly_budget > 0 else 0

    # Create a PDF file in memory
    pdf_buffer = io.BytesIO()
    pdf = canvas.Canvas(pdf_buffer, pagesize=letter)
    pdf.setTitle(f"Expense Report - {current_month_display}")

    # Header
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(200, 750, f"Expense Report - {current_month_display}")

    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, 720, f"Budget: ${monthly_budget if monthly_budget > 0 else 'Not Set'}")
    pdf.drawString(100, 700, f"Total Spent: ${total_spent}")
    pdf.drawString(100, 680, f"Remaining Budget: ${remaining_budget}")

    pdf.line(50, 660, 550, 660)  # Draw a line

    # Expense List Header
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, 640, "Date")
    pdf.drawString(150, 640, "Description")
    pdf.drawString(350, 640, "Category")
    pdf.drawString(450, 640, "Amount")

    pdf.line(50, 630, 550, 630)  # Draw a line

    # List expenses
    y_position = 610
    pdf.setFont("Helvetica", 10)
    for exp in current_month_expenses:
        pdf.drawString(50, y_position, exp["date"])
        pdf.drawString(150, y_position, exp["description"])
        pdf.drawString(350, y_position, exp["category"])
        pdf.drawString(450, y_position, f"${exp['amount']:.2f}")
        y_position -= 20
        if y_position < 50:
            pdf.showPage()  # Start a new page if running out of space
            y_position = 750

    pdf.save()

    # Return the PDF file for download
    pdf_buffer.seek(0)
    return send_file(pdf_buffer, mimetype="application/pdf", as_attachment=True, download_name=f"Expense_Report_{current_month}.pdf")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
