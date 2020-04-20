"""update admin and realm

Revision ID: f3bc7c5f757e
Revises: 
Create Date: 2020-03-27 23:14:15.933891

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f3bc7c5f757e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin',
    sa.Column('id_admin', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=32), nullable=True),
    sa.Column('last_name', sa.String(length=32), nullable=True),
    sa.Column('email', sa.String(length=128), nullable=True),
    sa.Column('password', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id_admin')
    )
    op.create_index(op.f('ix_admin_email'), 'admin', ['email'], unique=True)
    op.create_table('realm',
    sa.Column('id_realm', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=32), nullable=True),
    sa.Column('description', sa.String(length=256), nullable=True),
    sa.Column('admin_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['admin_id'], ['admin.id_admin'], ),
    sa.PrimaryKeyConstraint('id_realm'),
    sa.UniqueConstraint('description'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('realm')
    op.drop_index(op.f('ix_admin_email'), table_name='admin')
    op.drop_table('admin')
    # ### end Alembic commands ###