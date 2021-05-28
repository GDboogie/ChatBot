from sqlalchemy import (
    Column,
    BigInteger,
    VARCHAR,
    TEXT,
    ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.database import Base


class User(Base):
    __tablename__ = 'bot__user'

    uuid = Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)

    first_name = Column(VARCHAR(255), nullable=True, unique=False)
    user_name = Column(VARCHAR(255), nullable=True, unique=False)
    chat_id = Column(BigInteger, nullable=False, unique=True)

    message = relationship('Message', back_populates='user')


class Message(Base):
    __tablename__ = 'bot__message'

    uuid = Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)

    user_uuid = Column(UUID(as_uuid=True), ForeignKey('bot__user.uuid'), nullable=False)
    intent_uuid = Column(UUID(as_uuid=True), ForeignKey('bot__intent.uuid'), nullable=True)
    date = Column(BigInteger, nullable=False, unique=False)
    text = Column(TEXT, nullable=False, unique=False)

    user = relationship('User', back_populates='message')
    reply = relationship('Reply', back_populates='message')
    intent = relationship('Intent', back_populates='message')


class Reply(Base):
    __tablename__ = 'bot__reply'

    uuid = Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)

    message_uuid = Column(UUID(as_uuid=True), ForeignKey('bot__message.uuid'), nullable=False)
    text = Column(TEXT, nullable=False, unique=False)

    message = relationship('Message', back_populates='reply')


class Intent(Base):
    __tablename__ = 'bot__intent'

    uuid = Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    text = Column(TEXT, nullable=False, unique=False)
    response = Column(TEXT, nullable=False, unique=False)

    message = relationship('Message', back_populates='intent')
