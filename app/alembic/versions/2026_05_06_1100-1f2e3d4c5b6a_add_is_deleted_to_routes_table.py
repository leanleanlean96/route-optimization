"""add is_deleted column to routes table"""

from alembic import op
import sqlalchemy as sa


revision = "1f2e3d4c5b6a"
down_revision = "457a7d0e4443"
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = [column["name"] for column in inspector.get_columns("routes")]

    if "is_deleted" not in columns:
        op.add_column(
            "routes",
            sa.Column(
                "is_deleted",
                sa.Boolean(),
                nullable=False,
                server_default=sa.false(),
            ),
        )


def downgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = [column["name"] for column in inspector.get_columns("routes")]

    if "is_deleted" in columns:
        op.drop_column("routes", "is_deleted")