from flask import Flask
from config import Config
from extensions import db, login_manager, bcrypt

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    from routes.auth import auth
    from routes.dashboard import dashboard
    from routes.expense import expense
    from routes.income import income

    app.register_blueprint(auth)
    app.register_blueprint(dashboard)
    app.register_blueprint(expense)
    app.register_blueprint(income)

    with app.app_context():
        from models.user import User
        from models.expense import Expense
        from models.income import Income
        from models.budget import Budget
        db.create_all()

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
