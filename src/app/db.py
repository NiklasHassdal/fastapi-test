from os import getenv
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    UniqueConstraint,
)

engine = create_engine(getenv("DATABASE_URL"))
metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("email", String),
    Column("password", String),
    UniqueConstraint("email"),
)
