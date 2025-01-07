"""updating the appointments

Revision ID: e9080515ef7b
Revises: 17ec4bba93c8
Create Date: 2025-01-06 11:38:08.170704

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'e9080515ef7b'
down_revision: Union[str, None] = '17ec4bba93c8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.drop_column('appointment', 'customer_id')

def downgrade():
    op.add_column(
        'appointment',
        sa.Column('customer_id', sa.Integer, sa.ForeignKey('users.user_id'), nullable=True)
    )

    # ### end Alembic commands ###
