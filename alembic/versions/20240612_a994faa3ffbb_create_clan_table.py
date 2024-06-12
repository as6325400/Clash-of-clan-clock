"""create clan table

Revision ID: a994faa3ffbb
Revises: 
Create Date: 2024-06-12 12:54:47.357819

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a994faa3ffbb'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'clan',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('tag', sa.String(20), comment='部落tag'),
        sa.Column('name', sa.String(200), comment='部落名稱'),
    )


def downgrade() -> None:
    op.drop_table('clan')
