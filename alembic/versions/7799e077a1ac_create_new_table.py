"""create new table

Revision ID: 7799e077a1ac
Revises:
Create Date: 2025-06-01 17:14:09.015724

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7799e077a1ac"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "shit_table",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("shit name", sa.String()),
        sa.Column("shit_password", sa.String()),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("shit_table")
