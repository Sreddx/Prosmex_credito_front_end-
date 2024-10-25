from ..database import db
from datetime import datetime
import pytz

class Falta(db.Model):
    __tablename__ = 'falta'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('America/Mexico_City')), nullable=False)
    prestamo_id = db.Column(db.Integer, db.ForeignKey('prestamos.prestamo_id'), nullable=False)
    
    
    def serialize(self):
        return {
            'id': self.id,
            'fecha': self.fecha,
            'prestamo_id': self.prestamo_id
        }