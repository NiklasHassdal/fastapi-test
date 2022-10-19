"""Created user table

Revision ID: 10184b08f830
Revises: 
Create Date: 2022-10-18 19:10:43.099252

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '10184b08f830'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )


def downgrade() -> None:
    op.drop_table('users')
