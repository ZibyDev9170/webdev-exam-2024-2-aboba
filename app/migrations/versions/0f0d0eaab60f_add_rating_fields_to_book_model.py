"""Add rating fields to Book model

Revision ID: 0f0d0eaab60f
Revises: 2ae2246d1276
Create Date: 2024-06-13 23:33:04.474348

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0f0d0eaab60f'
down_revision = '2ae2246d1276'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.add_column(sa.Column('rating_count', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('rating_sum', sa.Integer(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.drop_column('rating_sum')
        batch_op.drop_column('rating_count')

    # ### end Alembic commands ###