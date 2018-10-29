from flask_migrate import Migrate
from flask_migrate import MigrateCommand
from flask_script import Manager
import os
from search_api.extensions import db
from search_api.main import app


migrate = Migrate(app, db)
# ***** For Alembic end ******

manager = Manager(app)

# ***** For Alembic start ******
manager.add_command('db', MigrateCommand)
# ***** For Alembic end ******


# ***** Custom commands start ******
@manager.command
def runserver(port=9798):
    """Run the app using flask server"""

    os.environ["PYTHONUNBUFFERED"] = "yes"
    os.environ["LOG_LEVEL"] = "DEBUG"
    os.environ["COMMIT"] = "LOCAL"

    app.run(debug=True, port=int(port))


if __name__ == "__main__":
    manager.run()
