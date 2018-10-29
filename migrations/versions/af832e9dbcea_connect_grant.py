"""Grant connect privileges

Revision ID: af832e9dbcea
Revises: 13544f557ab9
Create Date: 2017-09-01 11:10:08.001231

"""

# revision identifiers, used by Alembic.
revision = 'af832e9dbcea'
down_revision = '13544f557ab9'

from alembic import op
from flask import current_app


def upgrade():
    query = "GRANT CONNECT ON DATABASE {0} TO {1} ".format(current_app.config.get("SQL_DATABASE"),
                                                           current_app.config.get("FEEDER_SQL_USERNAME"))
    op.execute(query)


def downgrade():
    query = "REVOKE CONNECT ON DATABASE {0} FROM {1} ".format(current_app.config.get("SQL_DATABASE"),
                                                              current_app.config.get("FEEDER_SQL_USERNAME"))
    op.execute(query)
