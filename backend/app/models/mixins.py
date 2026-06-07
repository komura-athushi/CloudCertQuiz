from datetime import datetime

from sqlalchemy import text
from sqlalchemy.dialects import mysql
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.schema import FetchedValue

# created_at と updated_at を持つ Mixin クラス
class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        mysql.DATETIME(),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )

    updated_at: Mapped[datetime] = mapped_column(
        mysql.DATETIME(),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        server_onupdate=FetchedValue(),
    )
