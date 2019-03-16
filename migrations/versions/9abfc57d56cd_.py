"""empty message

Revision ID: 9abfc57d56cd
Revises: 
Create Date: 2019-03-16 17:35:16.814589

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9abfc57d56cd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('family',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=140), nullable=True),
    sa.Column('country', sa.String(length=50), nullable=True),
    sa.Column('location', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_family'))
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=False),
    sa.Column('password', sa.String(length=128), nullable=False),
    sa.Column('location', sa.String(length=128), nullable=False),
    sa.Column('current_family', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_user'))
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_user_username'), ['username'], unique=True)

    op.create_table('chat',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('family_id', sa.Integer(), nullable=True),
    sa.Column('room_id', sa.String(length=10), nullable=True),
    sa.ForeignKeyConstraint(['family_id'], ['family.id'], name=op.f('fk_chat_family_id_family')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_chat'))
    )
    op.create_table('cloud',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('family_id', sa.Integer(), nullable=True),
    sa.Column('dir_path', sa.String(length=200), nullable=True),
    sa.ForeignKeyConstraint(['family_id'], ['family.id'], name=op.f('fk_cloud_family_id_family')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_cloud'))
    )
    op.create_table('event',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(length=300), nullable=True),
    sa.Column('start', sa.String(length=100), nullable=False),
    sa.Column('end', sa.String(length=100), nullable=False),
    sa.Column('family_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['family_id'], ['family.id'], name=op.f('fk_event_family_id_family')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_event'))
    )
    op.create_table('family_identifier',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('family_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['family_id'], ['family.id'], name=op.f('fk_family_identifier_family_id_family')),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_family_identifier_user_id_user'))
    )
    op.create_table('join__request',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('requester_id', sa.Integer(), nullable=True),
    sa.Column('family_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['family_id'], ['family.id'], name=op.f('fk_join__request_family_id_family')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_join__request'))
    )
    op.create_table('list',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('elements', sa.String(length=1000), nullable=True),
    sa.Column('user', sa.String(length=50), nullable=False),
    sa.Column('date_time', sa.String(length=100), nullable=False),
    sa.Column('family_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['family_id'], ['family.id'], name=op.f('fk_list_family_id_family')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_list'))
    )
    op.create_table('reminder',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('family', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(length=100), nullable=False),
    sa.Column('date_time', sa.String(length=100), nullable=False),
    sa.Column('user', sa.String(length=50), nullable=False),
    sa.ForeignKeyConstraint(['family'], ['family.id'], name=op.f('fk_reminder_family_family')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_reminder'))
    )
    op.create_table('chat_message',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('chat_id', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.String(length=100), nullable=False),
    sa.Column('content', sa.String(length=400), nullable=False),
    sa.Column('username', sa.String(length=30), nullable=False),
    sa.ForeignKeyConstraint(['chat_id'], ['chat.id'], name=op.f('fk_chat_message_chat_id_chat')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_chat_message'))
    )
    op.create_table('file',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cloud_id', sa.Integer(), nullable=True),
    sa.Column('filename', sa.String(length=200), nullable=False),
    sa.Column('extension', sa.String(length=20), nullable=False),
    sa.Column('size', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=30), nullable=False),
    sa.Column('timestamp', sa.String(length=100), nullable=False),
    sa.ForeignKeyConstraint(['cloud_id'], ['cloud.id'], name=op.f('fk_file_cloud_id_cloud')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_file'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('file')
    op.drop_table('chat_message')
    op.drop_table('reminder')
    op.drop_table('list')
    op.drop_table('join__request')
    op.drop_table('family_identifier')
    op.drop_table('event')
    op.drop_table('cloud')
    op.drop_table('chat')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_username'))
        batch_op.drop_index(batch_op.f('ix_user_email'))

    op.drop_table('user')
    op.drop_table('family')
    # ### end Alembic commands ###
