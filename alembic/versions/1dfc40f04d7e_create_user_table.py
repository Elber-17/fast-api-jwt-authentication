"""create_user_table

Revision ID: 1dfc40f04d7e
Revises: 
Create Date: 2021-07-22 11:27:15.279891

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "1dfc40f04d7e"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "user",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("username", sa.VARCHAR(128), nullable=False),
        sa.Column("hashed_password", sa.VARCHAR(128), nullable=False),
    )


def downgrade():
    op.drop_table("user")
