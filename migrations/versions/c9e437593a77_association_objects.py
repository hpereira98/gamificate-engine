"""association objects

Revision ID: c9e437593a77
Revises: 106126e052b3
Create Date: 2020-04-10 18:29:58.056166

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c9e437593a77'
down_revision = '106126e052b3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_badge', sa.Column('id_badge', sa.Integer(), nullable=False))
    op.add_column('user_badge', sa.Column('id_user', sa.Integer(), nullable=False))
    op.drop_constraint('user_badge_ibfk_2', 'user_badge', type_='foreignkey')
    op.drop_constraint('user_badge_ibfk_1', 'user_badge', type_='foreignkey')
    op.create_foreign_key(None, 'user_badge', 'badge', ['id_badge'], ['id_badge'])
    op.create_foreign_key(None, 'user_badge', 'user', ['id_user'], ['id_user'])
    op.drop_column('user_badge', 'user_id')
    op.drop_column('user_badge', 'badge_id')
    op.add_column('user_reward', sa.Column('id_reward', sa.Integer(), nullable=False))
    op.add_column('user_reward', sa.Column('id_user', sa.Integer(), nullable=False))
    op.drop_constraint('user_reward_ibfk_1', 'user_reward', type_='foreignkey')
    op.drop_constraint('user_reward_ibfk_2', 'user_reward', type_='foreignkey')
    op.create_foreign_key(None, 'user_reward', 'reward', ['id_reward'], ['id_reward'])
    op.create_foreign_key(None, 'user_reward', 'user', ['id_user'], ['id_user'])
    op.drop_column('user_reward', 'user_id')
    op.drop_column('user_reward', 'reward_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_reward', sa.Column('reward_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))
    op.add_column('user_reward', sa.Column('user_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'user_reward', type_='foreignkey')
    op.drop_constraint(None, 'user_reward', type_='foreignkey')
    op.create_foreign_key('user_reward_ibfk_2', 'user_reward', 'user', ['user_id'], ['id_user'])
    op.create_foreign_key('user_reward_ibfk_1', 'user_reward', 'reward', ['reward_id'], ['id_reward'])
    op.drop_column('user_reward', 'id_user')
    op.drop_column('user_reward', 'id_reward')
    op.add_column('user_badge', sa.Column('badge_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))
    op.add_column('user_badge', sa.Column('user_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'user_badge', type_='foreignkey')
    op.drop_constraint(None, 'user_badge', type_='foreignkey')
    op.create_foreign_key('user_badge_ibfk_1', 'user_badge', 'badge', ['badge_id'], ['id_badge'])
    op.create_foreign_key('user_badge_ibfk_2', 'user_badge', 'user', ['user_id'], ['id_user'])
    op.drop_column('user_badge', 'id_user')
    op.drop_column('user_badge', 'id_badge')
    # ### end Alembic commands ###