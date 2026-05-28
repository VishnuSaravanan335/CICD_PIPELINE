from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models.expense import Expense
from models.income import Income
from models.budget import Budget
from sqlalchemy import func
from datetime import datetime

dashboard = Blueprint('dashboard', __name__)

@dashboard.route("/")
@dashboard.route("/dashboard")
@login_required
def home():
    # Calculate totals
    total_income = db.session.query(func.sum(Income.amount)).filter(Income.user_id == current_user.id).scalar() or 0
    total_expenses = db.session.query(func.sum(Expense.amount)).filter(Expense.user_id == current_user.id).scalar() or 0
    balance = total_income - total_expenses
    
    # Recent transactions
    recent_expenses = Expense.query.filter_by(user_id=current_user.id).order_by(Expense.date.desc()).limit(5).all()
    
    # Category-wise expenses for chart
    category_data = db.session.query(Expense.category, func.sum(Expense.amount)).filter(Expense.user_id == current_user.id).group_by(Expense.category).all()
    
    return render_template('dashboard.html', 
                           total_income=total_income, 
                           total_expenses=total_expenses, 
                           balance=balance,
                           recent_expenses=recent_expenses,
                           category_data=category_data,
                           now=datetime.utcnow())

@dashboard.route("/seed_data")
@login_required
def seed_data():
    from models.expense import Expense
    from models.income import Income
    import random
    from datetime import timedelta
    
    # Create mock income
    if not Income.query.filter_by(user_id=current_user.id).first():
        inc = Income(source="Core Salary", amount=8500.0, author=current_user, date=datetime.utcnow())
        db.session.add(inc)
    
    # Create mock expenses
    categories = ["Food", "Transport", "Rent", "Utilities", "Entertainment", "Shopping"]
    if not Expense.query.filter_by(user_id=current_user.id).first():
        for i in range(10):
            exp = Expense(
                amount=random.uniform(20, 500),
                category=random.choice(categories),
                description=f"Automated node transaction {i+1}",
                author=current_user,
                date=datetime.utcnow() - timedelta(days=random.randint(0, 30))
            )
            db.session.add(exp)
    
    db.session.commit()
    flash('System data seeded successfully. Analyzing trajectory...', 'success')
    return redirect(url_for('dashboard.home'))

@dashboard.route("/reports")
@login_required
def reports():
    # Detailed analytics
    category_data = db.session.query(Expense.category, func.sum(Expense.amount)).filter(Expense.user_id == current_user.id).group_by(Expense.category).all()
    
    # Monthly trend (last 6 months)
    monthly_data = db.session.query(func.strftime('%Y-%m', Expense.date), func.sum(Expense.amount)).filter(Expense.user_id == current_user.id).group_by(func.strftime('%Y-%m', Expense.date)).all()
    
    return render_template('reports.html', category_data=category_data, monthly_data=monthly_data)

from extensions import db # Import db here to avoid circular imports if needed, but it's already in extensions
