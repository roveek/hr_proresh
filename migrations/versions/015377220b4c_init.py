"""create db

Revision ID: 015377220b4c
Revises:
Create Date: 2026-01-21 17:14:52.149608

"""
from typing import Sequence
from typing import Union

from alembic import op
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = '015377220b4c'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # op.execute(text(
    #     """
    #     """
    # ))


def downgrade() -> None:
    """Downgrade schema."""
    # op.execute(text(
    #     """
    #     """
    # ))
