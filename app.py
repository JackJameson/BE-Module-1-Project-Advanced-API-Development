from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import date
from typing import List

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password@localhost/mechanic_shop_db'


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

db.init_app(app)

class Customer(Base):
    __tablename__ = 'customers'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(360), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(10), nullable=False)
    service_tickets: Mapped[List['ServiceTicket']] = db.relationship(back_populates='customer')
    
service_mechanic = db.Table(
    'service_mechanic',
    Base.metadata,
    db.Column('service_tickets_id', db.ForeignKey('service_tickets.id')),
    db.Column('mechanic_id', db.ForeignKey('mechanics.id'))
)

class ServiceTicket(Base):
    __tablename__ = 'service_tickets'

    id: Mapped[int] = mapped_column(primary_key=True)
    VIN: Mapped[str] = mapped_column(db.String(255), nullable=False)
    service_date: Mapped[date] = mapped_column(db.Date)
    service_desc: Mapped[str] = mapped_column(db.String(255), nullable=False)
    member_id: Mapped[int] = mapped_column(db.ForeignKey('customer.id'))
    member: Mapped['Customer'] = db.relationship(back_populates='service_tickets')
    mechanics: Mapped[List['Mechanic']] = db.relationship(secondary=service_mechanic, back_populates='service_tickets')
    
class Mechanic(Base):
    __tablename__ = "mechanics"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(255), nullable=False)
    phone: Mapped[str] = mapped_column(db.String(10), nullable=False)
    salary: Mapped[float] = mapped_column(db.Float, nullable=False)
    service_tickets: Mapped[List['ServiceTicket']] = db.relationship(secondary=service_mechanic, back_populates='mechanics')
    
with app.app_context():
	db.create_all()

app.run(debug=True)