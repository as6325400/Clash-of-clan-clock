"""create clan_group_realationship table

Revision ID: ca2c3e388c74
Revises: d784b62f1600
Create Date: 2024-06-12 13:31:36.469407

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ca2c3e388c74'
down_revision: Union[str, None] = 'd784b62f1600'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'clan_group_realationship',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('clan_id', sa.Integer, sa.ForeignKey('clan.id'), comment='部落id'),
        sa.Column('group_id', sa.Integer, sa.ForeignKey('linegroup.id'), comment='群組id'),
    )


def downgrade() -> None:
    op.drop_table('clan_group_realationship')
