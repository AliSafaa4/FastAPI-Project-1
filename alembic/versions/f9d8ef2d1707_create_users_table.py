"""create users table

Revision ID: f9d8ef2d1707
Revises: f4579688e209
Create Date: 2024-06-19 15:57:04.068288

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f9d8ef2d1707'
down_revision: Union[str, None] = 'f4579688e209'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users', sa.Column('id',sa.Integer, primary_key=True, nullable=False),
                             sa.Column('name',sa.String, nullable=False),
                             sa.Column('email',sa.String, nullable=False, unique=True),
                             sa.Column('password',sa.String, nullable=False),
                             sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False, server_default = sa.text('now()'))
                             )
    pass


def downgrade() -> None:
    op.drop_table('users')
