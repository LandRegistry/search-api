"""Creates user with elevated permissions for the acceptance tests.

Revision ID: 09ebaab850f1
Revises: b93933fa5fa4
Create Date: 2017-11-20 10:38:43.464703

"""

# revision identifiers, used by Alembic.
revision = '09ebaab850f1'
down_revision = 'b93933fa5fa4'

from alembic import op
from flask import current_app


def upgrade():
    query = "DO $$ BEGIN IF NOT EXISTS (SELECT FROM pg_catalog.pg_user WHERE usename = '{0}') THEN CREATE ROLE {0} " \
            "WITH LOGIN PASSWORD '{1}'; END IF; END $$;".format(current_app.config.get("ACCTEST_SQL_USERNAME"),
                                                                current_app.config.get("ACCTEST_SQL_PASSWORD"))
    op.execute(query)

    op.execute("GRANT SELECT, INSERT, UPDATE, DELETE ON local_land_charge TO {};".format(current_app.config.get("ACCTEST_SQL_USERNAME")))
    op.execute("GRANT SELECT, USAGE ON local_land_charge_id_seq TO {};".format(current_app.config.get("ACCTEST_SQL_USERNAME")))

    op.execute("GRANT SELECT, INSERT, UPDATE, DELETE ON local_land_charge_history TO {};".format(current_app.config.get("ACCTEST_SQL_USERNAME")))
    op.execute("GRANT SELECT, USAGE ON local_land_charge_history_id_seq TO {};".format(current_app.config.get("ACCTEST_SQL_USERNAME")))

    op.execute("GRANT SELECT, INSERT, UPDATE, DELETE ON geometry_feature TO {};".format(current_app.config.get("ACCTEST_SQL_USERNAME")))
    op.execute("GRANT SELECT, USAGE ON geometry_feature_id_seq TO {};".format(current_app.config.get("ACCTEST_SQL_USERNAME")))

    op.execute("GRANT SELECT ON statutory_provision TO " + current_app.config.get("ACCTEST_SQL_USERNAME"))
    op.execute("GRANT SELECT ON statutory_provision_id_seq TO " + current_app.config.get("ACCTEST_SQL_USERNAME"))


def downgrade():

    query = "DO $$ BEGIN IF EXISTS (SELECT FROM pg_catalog.pg_user WHERE usename = '{0}') " \
            "THEN " \
            "REVOKE ALL PRIVILEGES ON local_land_charge FROM {0}; " \
            "REVOKE ALL PRIVILEGES ON local_land_charge_id_seq FROM {0}; " \
            "REVOKE ALL PRIVILEGES ON local_land_charge_history FROM {0}; " \
            "REVOKE ALL PRIVILEGES ON local_land_charge_history_id_seq FROM {0}; " \
            "REVOKE ALL PRIVILEGES ON geometry_feature FROM {0}; " \
            "REVOKE ALL PRIVILEGES ON geometry_feature_id_seq FROM {0}; " \
            "REVOKE ALL PRIVILEGES ON statutory_provision FROM {0}; " \
            "REVOKE ALL PRIVILEGES ON statutory_provision_id_seq FROM {0}; " \
            "DROP ROLE {0}; " \
            "END IF; END $$;".format(current_app.config.get("ACCTEST_SQL_USERNAME"))

    op.execute(query)
