"""create user table

Revision ID: 36dff3e501f
Revises: None
Create Date: 2014-06-05 20:34:39.771964

"""

# revision identifiers, used by Alembic.
revision = '36dff3e501f'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String(250), nullable=False, unique=True),
        sa.Column('display_name', sa.String(50), nullable=False),
        sa.Column('salt', sa.String(128), nullable=False),
        sa.Column('password', sa.String(32), nullable=False)
    )


def downgrade():
    pass
