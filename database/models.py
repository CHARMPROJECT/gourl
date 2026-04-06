from .database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, Integer
import shortuuid
import time

def get_uuid(length=25):
    return shortuuid.ShortUUID().random(length=length)

class Url(Base):
    __tablename__ = 'urls'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    uid: Mapped[str] = mapped_column(default=lambda: get_uuid())
    code: Mapped[str] = mapped_column(default=lambda: get_uuid(5), unique=True)
    url: Mapped[str]
    created_at: Mapped[int] = mapped_column(BigInteger, default=lambda: int(time.time()))
