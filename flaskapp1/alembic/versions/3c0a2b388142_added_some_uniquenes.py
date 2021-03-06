"""added some uniqueness and deleted Post

Revision ID: 3c0a2b388142
Revises: 51a83e459c10
Create Date: 2013-10-21 20:27:11.619309

"""

# revision identifiers, used by Alembic.
revision = '3c0a2b388142'
down_revision = '51a83e459c10'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table(u'post')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table(u'post',
    sa.Column(u'id', sa.INTEGER(), server_default="nextval('post_id_seq'::regclass)", nullable=False),
    sa.Column(u'body', sa.VARCHAR(length=140), autoincrement=False, nullable=True),
    sa.Column(u'timestamp', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column(u'user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], [u'user.id'], name=u'post_user_id_fkey'),
    sa.PrimaryKeyConstraint(u'id', name=u'post_pkey')
    )
    ### end Alembic commands ###
