from ..database import db

class TipoPrestamo(db.Model):
    __tablename__ = 'tipos_prestamo'
    nombre = db.Column(db.String(50))
    tipo_prestamo_id = db.Column(db.Integer, primary_key=True)
    numero_semanas = db.Column(db.Integer)
    porcentaje_semanal = db.Column(db.Float)
    incumplimientos_tolerados = db.Column(db.Integer)
    pena_incumplimiento = db.Column(db.Numeric)
    limite_penalizaciones = db.Column(db.Integer)
    interes = db.Column(db.Float)

    def serialize(self):
        return {
            'nombre': self.nombre,
            'tipo_prestamo_id': self.tipo_prestamo_id,
            'numero_semanas': self.numero_semanas,
            'porcentaje_semanal': self.porcentaje_semanal,
            'incumplimientos_tolerados': self.incumplimientos_tolerados,
            'pena_incumplimiento': self.pena_incumplimiento,
            'limite_penalizaciones': self.limite_penalizaciones,
            'interes': self.interes
        }