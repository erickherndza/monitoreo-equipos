#!/usr/bin/env python3
"""
Script para crear datos de ejemplo en la base de datos
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.models.user import User, db
from src.models.equipo import Equipo
from src.main import app
from datetime import datetime, date

def create_sample_data():
    with app.app_context():
        # Crear usuario administrador
        admin_user = User.query.filter_by(email='admin@test.com').first()
        if not admin_user:
            admin_user = User(
                nombre='Administrador',
                email='admin@test.com'
            )
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            print("✓ Usuario administrador creado")
        else:
            print("✓ Usuario administrador ya existe")

        # Crear equipos de ejemplo
        equipos_ejemplo = [
            {
                'nombre': 'Excavadora CAT 320',
                'estado': 'Activo',
                'ubicacion_lat': 18.4861,
                'ubicacion_lng': -69.9312,
                'fecha_ultima_revision': date(2024, 12, 1)
            },
            {
                'nombre': 'Bulldozer D6T',
                'estado': 'En mantenimiento',
                'ubicacion_lat': 18.5204,
                'ubicacion_lng': -69.9441,
                'fecha_ultima_revision': date(2024, 11, 15)
            },
            {
                'nombre': 'Grúa Liebherr LTM 1050',
                'estado': 'Activo',
                'ubicacion_lat': 18.4682,
                'ubicacion_lng': -69.9036,
                'fecha_ultima_revision': date(2024, 12, 10)
            },
            {
                'nombre': 'Camión Volvo FMX',
                'estado': 'Inactivo',
                'ubicacion_lat': 18.5001,
                'ubicacion_lng': -69.9886,
                'fecha_ultima_revision': date(2024, 10, 20)
            },
            {
                'nombre': 'Retroexcavadora JCB 3CX',
                'estado': 'Activo',
                'ubicacion_lat': 18.4565,
                'ubicacion_lng': -69.9507,
                'fecha_ultima_revision': date(2024, 12, 5)
            }
        ]

        for equipo_data in equipos_ejemplo:
            equipo_existente = Equipo.query.filter_by(nombre=equipo_data['nombre']).first()
            if not equipo_existente:
                nuevo_equipo = Equipo(**equipo_data)
                db.session.add(nuevo_equipo)
                print(f"✓ Equipo '{equipo_data['nombre']}' creado")
            else:
                print(f"✓ Equipo '{equipo_data['nombre']}' ya existe")

        # Guardar cambios
        db.session.commit()
        print("\n🎉 Datos de ejemplo creados exitosamente!")
        print("\nCredenciales de acceso:")
        print("Email: admin@test.com")
        print("Contraseña: admin123")

if __name__ == '__main__':
    create_sample_data()

