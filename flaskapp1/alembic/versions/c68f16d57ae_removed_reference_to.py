"""Removed reference to Post in User

Revision ID: c68f16d57ae
Revises: 3c0a2b388142
Create Date: 2013-10-21 20:38:41.121323

"""

# revision identifiers, used by Alembic.
revision = 'c68f16d57ae'
down_revision = '3c0a2b388142'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', u'hobby')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column(u'hobby', sa.VARCHAR(length=150), nullable=True))
    ### end Alembic commands ###
