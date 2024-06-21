"""create post table

Revision ID: f4579688e209
Revises: 
Create Date: 2024-06-19 15:49:07.413441

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f4579688e209'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id',sa.Integer, primary_key=True, nullable=False),
                             sa.Column('title',sa.String, nullable=False),
                             sa.Column('content',sa.String, nullable=False),
                             sa.Column('published',sa.Boolean, server_default = 'TRUE'),
                             sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False, server_default = sa.text('now()'))
                             )
    
    pass


def downgrade() -> None:
    op.drop_table('posts')
