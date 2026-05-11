from extensions import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    expenses = db.relationship('Expense', backref='author', lazy=True)
    incomes = db.relationship('Income', backref='author', lazy=True)
    budgets = db.relationship('Budget', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
