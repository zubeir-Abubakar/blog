#!/usr/bin/env python
from app import create_app, db
from app.models import User, Comments, Blog, Votes, BlogCategory, Quote
from flask_script import Manager,Server
from flask_migrate import Migrate, MigrateCommand

# Creating app instance
app = create_app('development')

manager = Manager(app)

manager.add_command('server', Server)
@manager.shell
def make_shell_context():
    return dict(app=app, db=db, User=User, Comments=Comments, Blog=Blog, Votes=Votes, BlogCategory=BlogCategory, Quote=quote)


migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    app.secret_key = 'zubeyr'
    manager.run()
