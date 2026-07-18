"""add status

Revision ID: ba1fb5820d05
Revises: ba1fb5820d04
Create Date: 2026-07-18 22:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ba1fb5820d05'
down_revision: Union[str, Sequence[str], None] = 'ba1fb5820d04'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('reviews', sa.Column('status', sa.String(), nullable=True, server_default="Processing"))


def downgrade() -> None:
    op.drop_column('reviews', 'status')
