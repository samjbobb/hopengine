from config import SQLALCHEMY_DATABASE_URI
from app import db

# create the tables
db.create_all()

# then lad the alembic config and generate the version table,
# "stamping" it with the most recent rev:
from alembic.config import Config
from alembic import command
alembic_cfg = Config('alembic.ini') # look for config in the cwd
command.stamp(alembic_cfg, "head")
