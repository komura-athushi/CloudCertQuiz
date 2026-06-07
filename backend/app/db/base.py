from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase


convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

# Base クラスを定義
# 継承されたモデルは、Base.metadataを通じてこの命名規約を使用する
# この命名規則がAlembicの自動生成機能で使用される
class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=convention)
