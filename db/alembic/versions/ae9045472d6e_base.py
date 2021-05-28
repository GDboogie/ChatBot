"""base

Revision ID: ae9045472d6e
Revises: 7f1ad0bdf797
Create Date: 2021-05-25 13:33:23.787544

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'ae9045472d6e'
down_revision = '7f1ad0bdf797'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'bot__intent', ['uuid'])
    op.alter_column('bot__message', 'intent_uuid',
               existing_type=postgresql.UUID(),
               nullable=True)
    op.create_unique_constraint(None, 'bot__message', ['uuid'])
    op.create_unique_constraint(None, 'bot__reply', ['uuid'])
    op.create_unique_constraint(None, 'bot__user', ['uuid'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'bot__user', type_='unique')
    op.drop_constraint(None, 'bot__reply', type_='unique')
    op.drop_constraint(None, 'bot__message', type_='unique')
    op.alter_column('bot__message', 'intent_uuid',
               existing_type=postgresql.UUID(),
               nullable=False)
    op.drop_constraint(None, 'bot__intent', type_='unique')
    # ### end Alembic commands ###
