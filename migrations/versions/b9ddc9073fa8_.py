"""empty message

Revision ID: b9ddc9073fa8
Revises: fbc54a70330f
Create Date: 2021-12-23 13:01:55.136645

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b9ddc9073fa8'
down_revision = 'fbc54a70330f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('interviews', sa.Column('start_date', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('interviews', 'start_date')
    # ### end Alembic commands ###
