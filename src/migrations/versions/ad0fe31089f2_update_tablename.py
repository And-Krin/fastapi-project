"""update tablename

Revision ID: ad0fe31089f2
Revises: 7e222881b3ce
Create Date: 2023-06-04 17:56:32.613672

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'ad0fe31089f2'
down_revision = '7e222881b3ce'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.rename_table('user', 'users')

    op.rename_table('item', 'items')


def downgrade() -> None:
    op.rename_table('users', 'user')

    op.rename_table('items', 'item')
