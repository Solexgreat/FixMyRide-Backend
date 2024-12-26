"""Update user_type enum

Revision ID: 17ec4bba93c8
Revises: 
Create Date: 2024-12-26 13:45:24.136189

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '17ec4bba93c8'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add 'mechanic' to the enum
    op.execute("""
        ALTER TYPE user_type_enum ADD VALUE 'mechanic';
    """)

def downgrade() -> None:
    # Downgrading enums isn't straightforward; it requires a new type creation.
    op.execute("""
        CREATE TYPE user_type_enum_tmp AS ENUM('admin', 'user', 'guest');
        ALTER TABLE users ALTER COLUMN user_type TYPE user_type_enum_tmp USING user_type::text::user_type_enum_tmp;
        DROP TYPE user_type_enum;
        ALTER TYPE user_type_enum_tmp RENAME TO user_type_enum;
    """)