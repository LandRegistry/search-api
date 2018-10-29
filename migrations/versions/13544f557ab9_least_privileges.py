"""Setup least privileges and create user for feeder to use

Revision ID: 13544f557ab9
Revises: 983417fd8ca1
Create Date: 2017-08-17 12:48:47.044963

"""

# revision identifiers, used by Alembic.
revision = '13544f557ab9'
down_revision = '983417fd8ca1'

from alembic import op
from flask import current_app


def upgrade():

    op.execute("GRANT SELECT ON light_obstruction_notice TO " + current_app.config.get("APP_SQL_USERNAME"))
    op.execute("GRANT SELECT ON local_land_charge TO " + current_app.config.get("APP_SQL_USERNAME"))

    query = "DO $$ BEGIN IF NOT EXISTS (SELECT FROM pg_catalog.pg_user WHERE usename = '{0}') THEN CREATE ROLE {0} " \
            "WITH LOGIN PASSWORD '{1}'; END IF; END $$;".format(current_app.config.get("FEEDER_SQL_USERNAME"),
                                                                current_app.config.get("FEEDER_SQL_PASSWORD"))
    op.execute(query)

    op.execute("GRANT SELECT, INSERT, UPDATE, DELETE ON local_land_charge TO {};".format(current_app.config.get("FEEDER_SQL_USERNAME")))
    op.execute("GRANT SELECT, USAGE ON local_land_charge_id_seq TO {};".format(current_app.config.get("FEEDER_SQL_USERNAME")))

    op.execute("GRANT SELECT, INSERT, UPDATE, DELETE ON local_land_charge_history TO {};".format(current_app.config.get("FEEDER_SQL_USERNAME")))
    op.execute("GRANT SELECT, USAGE ON local_land_charge_history_id_seq TO {};".format(current_app.config.get("FEEDER_SQL_USERNAME")))

    op.execute("GRANT SELECT, INSERT, UPDATE, DELETE ON geometry_feature TO {};".format(current_app.config.get("FEEDER_SQL_USERNAME")))
    op.execute("GRANT SELECT, USAGE ON geometry_feature_id_seq TO {};".format(current_app.config.get("FEEDER_SQL_USERNAME")))

    op.execute("GRANT SELECT, INSERT, UPDATE, DELETE ON light_obstruction_notice TO {};".format(current_app.config.get("FEEDER_SQL_USERNAME")))


def downgrade():
    op.execute("GRANT ALL ON ALL TABLES IN SCHEMA public TO " + current_app.config.get("APP_SQL_USERNAME"))
    op.execute("GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO " + current_app.config.get("APP_SQL_USERNAME"))

    op.execute("REVOKE ALL PRIVILEGES ON local_land_charge FROM {};".format(current_app.config.get("FEEDER_SQL_USERNAME")))
    op.execute("REVOKE ALL PRIVILEGES ON local_land_charge_id_seq FROM {};".format(current_app.config.get("FEEDER_SQL_USERNAME")))

    op.execute("REVOKE ALL PRIVILEGES ON local_land_charge_history FROM {};".format(current_app.config.get("FEEDER_SQL_USERNAME")))
    op.execute("REVOKE ALL PRIVILEGES ON local_land_charge_history_id_seq FROM {};".format(current_app.config.get("FEEDER_SQL_USERNAME")))

    op.execute("REVOKE ALL PRIVILEGES ON geometry_feature FROM {};".format(current_app.config.get("FEEDER_SQL_USERNAME")))
    op.execute("REVOKE ALL PRIVILEGES ON geometry_feature_id_seq FROM {};".format(current_app.config.get("FEEDER_SQL_USERNAME")))

    op.execute("REVOKE ALL PRIVILEGES ON light_obstruction_notice FROM {};".format(current_app.config.get("FEEDER_SQL_USERNAME")))

    op.execute("DROP ROLE {};".format(current_app.config.get("FEEDER_SQL_USERNAME")))

