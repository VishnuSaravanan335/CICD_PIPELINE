from flask import Blueprint, render_template, url_for, flash, redirect, request
from extensions import db
from models.expense import Expense
from flask_login import login_required, current_user
from datetime import datetime

expense = Blueprint('expense', __name__)

@expense.route("/expenses", methods=['GET', 'POST'])
@login_required
def list_expenses():
    if request.method == 'POST':
        amount = float(request.form.get('amount'))
        category = request.form.get('category')
        description = request.form.get('description')
        date_str = request.form.get('date')
        date = datetime.strptime(date_str, '%Y-%m-%d') if date_str else datetime.utcnow()
        
        new_expense = Expense(amount=amount, category=category, description=description, date=date, author=current_user)
        db.session.add(new_expense)
        db.session.commit()
        flash('Expense added successfully!', 'success')
        return redirect(url_for('expense.list_expenses'))
        
    expenses = Expense.query.filter_by(user_id=current_user.id).order_by(Expense.date.desc()).all()
    return render_template('expenses.html', expenses=expenses, now=datetime.utcnow())

@expense.route("/expense/delete/<int:expense_id>", methods=['POST'])
@login_required
def delete_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    if expense.author != current_user:
        flash('You do not have permission to delete this expense', 'danger')
        return redirect(url_for('expense.list_expenses'))
    db.session.delete(expense)
    db.session.commit()
    flash('Expense deleted!', 'success')
    return redirect(url_for('expense.list_expenses'))
