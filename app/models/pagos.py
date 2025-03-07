from dataclasses import dataclass

from app import db


@dataclass
class Pagos(db.Model):
    __tablename__ = 'Pagos'

    id: int = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    producto_id: int = db.Column('producto_id', db.Integer, nullable=False)
    precio: int = db.Column('precio', db.Integer, nullable=False)
    medio_pago: str = db.Column('medio_pago', db.Text, nullable=False)

