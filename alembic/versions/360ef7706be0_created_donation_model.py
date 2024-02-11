"""Created Donation model

Revision ID: 360ef7706be0
Revises: 800b5ada63f1
Create Date: 2024-01-27 17:39:44.255405

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '360ef7706be0'
down_revision = '800b5ada63f1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('donation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('comment', sa.Text(), nullable=True),
    sa.Column('full_amount', sa.Integer(), nullable=False),
    sa.Column('invested_amount', sa.Integer(), nullable=True),
    sa.Column('fully_invested', sa.Boolean(), nullable=False),
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.Column('close_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('donation')
    # ### end Alembic commands ###