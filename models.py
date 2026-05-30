from typing import Optional
import datetime
import decimal

from sqlalchemy import Column, DECIMAL, DateTime, ForeignKeyConstraint, Index, String, Table
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class Country(Base):
    __tablename__ = 'country'

    country_id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    country_name: Mapped[str] = mapped_column(String(100), nullable=False)

    film: Mapped[list['Film']] = relationship('Film', secondary='film_country', back_populates='country')


class Film(Base):
    __tablename__ = 'film'

    film_id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    year: Mapped[int] = mapped_column(INTEGER(11), nullable=False)
    director: Mapped[str] = mapped_column(String(100), nullable=False)
    duration_mins: Mapped[int] = mapped_column(INTEGER(11), nullable=False)
    description: Mapped[str] = mapped_column(String(1000), nullable=False)
    rating: Mapped[Optional[decimal.Decimal]] = mapped_column(DECIMAL(10, 1))

    country: Mapped[list['Country']] = relationship('Country', secondary='film_country', back_populates='film')
    genre: Mapped[list['Genre']] = relationship('Genre', secondary='film_genre', back_populates='film')
    session: Mapped[list['Session']] = relationship('Session', back_populates='film')


class Genre(Base):
    __tablename__ = 'genre'

    genre_id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    genre_name: Mapped[str] = mapped_column(String(100), nullable=False)

    film: Mapped[list['Film']] = relationship('Film', secondary='film_genre', back_populates='genre')


class Hall(Base):
    __tablename__ = 'hall'

    hall_id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    row_count: Mapped[int] = mapped_column(INTEGER(11), nullable=False)
    places_in_row: Mapped[int] = mapped_column(INTEGER(11), nullable=False)
    hall_name: Mapped[str] = mapped_column(String(100), nullable=False)

    session: Mapped[list['Session']] = relationship('Session', back_populates='hall')


class User(Base):
    __tablename__ = 'user'

    user_id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    login: Mapped[str] = mapped_column(String(100), nullable=False)
    hashPassword: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(50), nullable=False)

    ticket: Mapped[list['Ticket']] = relationship('Ticket', back_populates='user')


t_film_country = Table(
    'film_country', Base.metadata,
    Column('ID_country', INTEGER(11), primary_key=True),
    Column('ID_film', INTEGER(11), primary_key=True),
    ForeignKeyConstraint(['ID_country'], ['country.country_id'], ondelete='CASCADE', onupdate='CASCADE', name='film_country_ibfk_1'),
    ForeignKeyConstraint(['ID_film'], ['film.film_id'], ondelete='CASCADE', onupdate='CASCADE', name='film_country_ibfk_2'),
    Index('ID_film', 'ID_film'),
    Index('film_country_pkfk', 'ID_country', 'ID_film')
)



t_film_genre = Table(
    'film_genre', Base.metadata,
    Column('ID_genre', INTEGER(11), primary_key=True),
    Column('ID_film', INTEGER(11), primary_key=True),
    ForeignKeyConstraint(['ID_film'], ['film.film_id'], ondelete='CASCADE', onupdate='CASCADE', name='film_genre_ibfk_1'),
    ForeignKeyConstraint(['ID_genre'], ['genre.genre_id'], ondelete='CASCADE', onupdate='CASCADE', name='film_genre_ibfk_2'),
    Index('ID_film', 'ID_film'),
    Index('film_genre_pkfk', 'ID_genre', 'ID_film')
)


class Session(Base):
    __tablename__ = 'session'
    __table_args__ = (
        ForeignKeyConstraint(['ID_film'], ['film.film_id'], ondelete='CASCADE', onupdate='CASCADE', name='session_ibfk_1'),
        ForeignKeyConstraint(['ID_hall'], ['hall.hall_id'], ondelete='CASCADE', onupdate='CASCADE', name='session_ibfk_2'),
        Index('session_film_fk', 'ID_film'),
        Index('session_hall_fk', 'ID_hall')
    )

    session_id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    session_datetime: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    price: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 0), nullable=False)
    ID_film: Mapped[int] = mapped_column(INTEGER(11), nullable=False)
    ID_hall: Mapped[int] = mapped_column(INTEGER(11), nullable=False)

    film: Mapped['Film'] = relationship('Film', back_populates='session')
    hall: Mapped['Hall'] = relationship('Hall', back_populates='session')
    seat: Mapped[list['Seat']] = relationship('Seat', back_populates='session')
    ticket: Mapped[list['Ticket']] = relationship('Ticket', back_populates='session')


class Seat(Base):
    __tablename__ = 'seat'
    __table_args__ = (
        ForeignKeyConstraint(['ID_session'], ['session.session_id'], ondelete='CASCADE', onupdate='CASCADE', name='seat_ibfk_1'),
        Index('seat_session_fk', 'ID_session')
    )

    seat_id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    row: Mapped[int] = mapped_column(INTEGER(11), nullable=False)
    place: Mapped[int] = mapped_column(INTEGER(11), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    ID_session: Mapped[int] = mapped_column(INTEGER(11), nullable=False)

    session: Mapped['Session'] = relationship('Session', back_populates='seat')


class Ticket(Base):
    __tablename__ = 'ticket'
    __table_args__ = (
        ForeignKeyConstraint(['ID_session'], ['session.session_id'], ondelete='CASCADE', onupdate='CASCADE', name='ticket_ibfk_1'),
        ForeignKeyConstraint(['ID_user'], ['user.user_id'], ondelete='CASCADE', onupdate='CASCADE', name='ticket_ibfk_2'),
        Index('ticket_session_fk', 'ID_session'),
        Index('ticket_user_fk', 'ID_user')
    )

    ticket_id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    purchase_datetime: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    ID_session: Mapped[int] = mapped_column(INTEGER(11), nullable=False)
    ID_user: Mapped[int] = mapped_column(INTEGER(11), nullable=False)

    session: Mapped['Session'] = relationship('Session', back_populates='ticket')
    user: Mapped['User'] = relationship('User', back_populates='ticket')
