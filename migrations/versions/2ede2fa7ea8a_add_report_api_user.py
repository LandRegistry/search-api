"""Set-up user with least privileges for report-api

Revision ID: 2ede2fa7ea8a
Revises: f35534934918
Create Date: 2018-06-27 16:14:32.713316

"""

# revision identifiers, used by Alembic.
revision = '2ede2fa7ea8a'
down_revision = 'f35534934918'

from alembic import op
from flask import current_app


def upgrade():
    query = "DO $$ BEGIN IF NOT EXISTS (SELECT FROM pg_catalog.pg_user WHERE usename = '{0}') THEN CREATE ROLE {0} " \
            "WITH LOGIN PASSWORD '{1}'; END IF; END $$;".format(current_app.config.get("REPORT_API_SQL_USERNAME"),
                                                                current_app.config.get("REPORT_API_SQL_PASSWORD"))
    op.execute(query)
    op.execute("GRANT SELECT ON local_land_charge_history TO {};"
               .format(current_app.config.get("REPORT_API_SQL_USERNAME")))


def downgrade():
    op.execute("REVOKE SELECT ON local_land_charge_history FROM {};"
               .format(current_app.config.get("REPORT_API_SQL_USERNAME")))
    query = "DO $$ BEGIN IF EXISTS (SELECT FROM pg_catalog.pg_user WHERE usename = '{0}') THEN DROP ROLE {0};" \
            " END IF; END $$;".format(current_app.config.get("REPORT_API_SQL_USERNAME"))
    op.execute(query)