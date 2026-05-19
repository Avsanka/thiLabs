from typing import Optional

from sqlalchemy import ForeignKeyConstraint, Index, String
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = 'users'

    user_ID: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    surname: Mapped[str] = mapped_column(String(30), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(50))

    reviews: Mapped[list['Reviews']] = relationship('Reviews', back_populates='users')


class Reviews(Base):
    __tablename__ = 'reviews'
    __table_args__ = (
        ForeignKeyConstraint(['ID_User'], ['users.user_ID'], ondelete='CASCADE', onupdate='CASCADE', name='reviews_ibfk_1'),
        Index('review_user_fk', 'ID_User')
    )

    review_ID: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    ID_User: Mapped[int] = mapped_column(INTEGER(11), nullable=False)
    content: Mapped[str] = mapped_column(String(500), nullable=False)

    users: Mapped['Users'] = relationship('Users', back_populates='reviews')
