from src.models.user import db
from datetime import datetime

class Equipo(db.Model):
    __tablename__ = 'equipos'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.String(50), nullable=False, default='Activo')  # Activo, Inactivo, En mantenimiento
    ubicacion_lat = db.Column(db.Float, nullable=True)
    ubicacion_lng = db.Column(db.Float, nullable=True)
    fecha_ultima_revision = db.Column(db.Date, nullable=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'estado': self.estado,
            'ubicacion_lat': self.ubicacion_lat,
            'ubicacion_lng': self.ubicacion_lng,
            'fecha_ultima_revision': self.fecha_ultima_revision.isoformat() if self.fecha_ultima_revision else None,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'fecha_actualizacion': self.fecha_actualizacion.isoformat() if self.fecha_actualizacion else None
        }
    
    def __repr__(self):
        return f'<Equipo {self.nombre}>'

