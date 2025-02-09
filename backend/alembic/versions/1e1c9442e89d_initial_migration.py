"""Initial migration

Revision ID: 1e1c9442e89d
Revises:
Create Date: 2025-02-09 14:34:38.844736

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = "1e1c9442e89d"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "project",
        sa.Column("id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("description", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("link", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("is_private", sa.Boolean(), nullable=False),
        sa.Column("last_entry_date", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_project_name"), "project", ["name"], unique=False)
    op.create_table(
        "technology",
        sa.Column("id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("description", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column(
            "language",
            sa.Enum("PYTHON", "JAVASCRIPT", "TYPESCRIPT", "GO", name="language"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_technology_language"), "technology", ["language"], unique=False
    )
    op.create_index(op.f("ix_technology_name"), "technology", ["name"], unique=False)
    op.create_table(
        "journal_entry",
        sa.Column("id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("content", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("date", sa.DateTime(), nullable=False),
        sa.Column("is_private", sa.Boolean(), nullable=False),
        sa.Column("project_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["project.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_journal_entry_project_id"),
        "journal_entry",
        ["project_id"],
        unique=False,
    )
    op.create_table(
        "journalentrytechnologylink",
        sa.Column(
            "journal_entry_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False
        ),
        sa.Column("technology_id", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.ForeignKeyConstraint(
            ["journal_entry_id"],
            ["journal_entry.id"],
        ),
        sa.ForeignKeyConstraint(
            ["technology_id"],
            ["technology.id"],
        ),
        sa.PrimaryKeyConstraint("journal_entry_id", "technology_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("journalentrytechnologylink")
    op.drop_index(op.f("ix_journal_entry_project_id"), table_name="journal_entry")
    op.drop_table("journal_entry")
    op.drop_index(op.f("ix_technology_name"), table_name="technology")
    op.drop_index(op.f("ix_technology_language"), table_name="technology")
    op.drop_table("technology")
    op.drop_index(op.f("ix_project_name"), table_name="project")
    op.drop_table("project")
    # ### end Alembic commands ###
