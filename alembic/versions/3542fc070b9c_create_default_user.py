"""create_default_user

Revision ID: 3542fc070b9c
Revises: 1dfc40f04d7e
Create Date: 2021-07-22 11:35:04.468232

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer


# revision identifiers, used by Alembic.
revision = "3542fc070b9c"
down_revision = "1dfc40f04d7e"
branch_labels = None
depends_on = None


def upgrade():
    accounts_table = table(
        "user",
        column("id", Integer),
        column("username", String),
        column("hashed_password", String),
    )

    op.bulk_insert(
        accounts_table,
        [
            {
                "id": 1,
                "username": "admin",
                "hashed_password": "$2b$12$Zl0ZY/sNzABjDrmQYZKj2ej3kYbIP5T6IOlyQVxYjricuvGi/hUBm",
            },
        ],
    )


def downgrade():
    op.execute("delete from user where name = 'admin';")
