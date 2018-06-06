"""empty message

Revision ID: 9fe68f574b8a
Revises: 283241ace598
Create Date: 2018-05-29 18:51:31.655115

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9fe68f574b8a'
down_revision = '283241ace598'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('translems', 'topic_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('translems', 'topic_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
