"""add user_id column to posts table

Revision ID: db3dbfe1785a
Revises: f9d8ef2d1707
Create Date: 2024-06-19 16:54:28.894123

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'db3dbfe1785a'
down_revision: Union[str, None] = 'f9d8ef2d1707'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('user_id',sa.Integer, sa.ForeignKey("users.id", ondelete = "CASCADE", onupdate = "CASCADE"), nullable = False))


def downgrade() -> None:
    op.drop_column('user_id')
