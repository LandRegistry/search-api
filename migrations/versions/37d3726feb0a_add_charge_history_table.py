"""Update LLC Register to add Charge History table

Revision ID: 37d3726feb0a
Revises: 2282351403f3
Create Date: 2017-04-12 11:23:50.439820

"""

# revision identifiers, used by Alembic.
revision = '37d3726feb0a'
down_revision = '2282351403f3'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from flask import current_app


def upgrade():
    op.create_table('local_land_charge_history',
                    sa.Column('id', sa.BigInteger(), primary_key=True),
                    sa.Column('llc_item', postgresql.JSONB(), nullable=False),
                    sa.Column('entry_number', sa.BigInteger(), primary_key=True),
                    sa.Column('cancelled', sa.Boolean(), nullable=False))
    op.execute("GRANT SELECT ON local_land_charge_history TO " +
                    current_app.config.get("APP_SQL_USERNAME"))
    op.execute("GRANT SELECT ON local_land_charge_history_id_seq TO " +
                    current_app.config.get("APP_SQL_USERNAME"))



def downgrade():
    op.drop_table('local_land_charge_history')
