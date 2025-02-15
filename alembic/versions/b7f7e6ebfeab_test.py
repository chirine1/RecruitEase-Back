"""test

Revision ID: b7f7e6ebfeab
Revises: c58816d6e760
Create Date: 2024-06-02 22:34:41.431692

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = 'b7f7e6ebfeab'
down_revision = 'c58816d6e760'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'blog_post', 'user', ['creator_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'blog_post', type_='foreignkey')
    # ### end Alembic commands ###
