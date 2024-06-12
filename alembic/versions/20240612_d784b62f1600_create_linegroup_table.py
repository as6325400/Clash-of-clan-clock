"""create linegroup table

Revision ID: d784b62f1600
Revises: a994faa3ffbb
Create Date: 2024-06-12 13:29:39.392453

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd784b62f1600'
down_revision: Union[str, None] = 'a994faa3ffbb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'linegroup',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('group_id', sa.String(200), comment='群組id'),
    )


def downgrade() -> None:
    op.drop_table('linegroup')
