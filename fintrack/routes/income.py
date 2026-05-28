from flask import Blueprint, render_template, url_for, flash, redirect, request
from extensions import db
from models.income import Income
from flask_login import login_required, current_user
from datetime import datetime

income = Blueprint('income', __name__)

@income.route("/income", methods=['GET', 'POST'])
@login_required
def list_income():
    if request.method == 'POST':
        amount = float(request.form.get('amount'))
        source = request.form.get('source')
        date_str = request.form.get('date')
        date = datetime.strptime(date_str, '%Y-%m-%d') if date_str else datetime.utcnow()
        
        new_income = Income(amount=amount, source=source, date=date, author=current_user)
        db.session.add(new_income)
        db.session.commit()
        flash('Income added successfully!', 'success')
        return redirect(url_for('income.list_income'))
        
    incomes = Income.query.filter_by(user_id=current_user.id).order_by(Income.date.desc()).all()
    return render_template('income.html', incomes=incomes, now=datetime.utcnow())

@income.route("/income/delete/<int:income_id>", methods=['POST'])
@login_required
def delete_income(income_id):
    income = Income.query.get_or_404(income_id)
    if income.author != current_user:
        flash('You do not have permission to delete this record', 'danger')
        return redirect(url_for('income.list_income'))
    db.session.delete(income)
    db.session.commit()
    flash('Income record deleted!', 'success')
    return redirect(url_for('income.list_income'))
