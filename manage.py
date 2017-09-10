#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask_script import Manager,Shell
from flask_migrate import Migrate, MigrateCommand
from app import create_app, db
from app.models import User

app = create_app('default')
manager = Manager(app)

#使用Migrate绑定app和db
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, User=User)
manager.add_command("shell", Shell(make_context=make_shell_context))
#添加迁移的命令到manager中
manager.add_command('db', MigrateCommand)

# 自定义命令
@manager.command
def test():
    """Run unit test"""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
    manager.run()
