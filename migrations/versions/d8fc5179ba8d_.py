"""empty message

Revision ID: d8fc5179ba8d
Revises: None
Create Date: 2016-05-31 00:56:29.500000

"""

# revision identifiers, used by Alembic.
revision = 'd8fc5179ba8d'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('valve_test_report', sa.Column('comments', sa.String(length=512), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('valve_test_report', 'comments')
    ### end Alembic commands ###