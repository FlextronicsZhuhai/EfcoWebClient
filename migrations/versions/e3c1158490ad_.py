"""empty message

Revision ID: e3c1158490ad
Revises: None
Create Date: 2016-06-04 16:13:32.596000

"""

# revision identifiers, used by Alembic.
revision = 'e3c1158490ad'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('valve_test_report', sa.Column('leakageUnit', sa.String(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('valve_test_report', 'leakageUnit')
    ### end Alembic commands ###
