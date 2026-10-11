"""Change servers name unique constraint to owner_id and name

Revision ID: 1a5b632a8fb1
Revises: 4032dbea90c9
Create Date: 2026-10-11 18:44:11.266515

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1a5b632a8fb1'
down_revision: Union[str, Sequence[str], None] = '4032dbea90c9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # SQLite requires batch mode for constraint changes (copy-and-move strategy)
    with op.batch_alter_table('servers', schema=None) as batch_op:
        batch_op.drop_index(op.f('ix_servers_name'))
        batch_op.create_index(op.f('ix_servers_name'), ['name'], unique=False)
        batch_op.create_unique_constraint('uq_servers_owner_id_name', ['owner_id', 'name'])


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('servers', schema=None) as batch_op:
        batch_op.drop_constraint('uq_servers_owner_id_name', type_='unique')
        batch_op.drop_index(op.f('ix_servers_name'))
        batch_op.create_index(op.f('ix_servers_name'), ['name'], unique=True)
