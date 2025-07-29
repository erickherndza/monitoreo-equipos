import logging
from flask import Blueprint, request, jsonify
from src.models.equipo import Equipo
from src.models.user import db
from datetime import datetime, date

equipo_bp = Blueprint("equipo", __name__)

logger = logging.getLogger(__name__)

@equipo_bp.route("/equipos", methods=["GET"])
def get_equipos():
    """Obtener todos los equipos"""
    try:
        equipos = Equipo.query.all()
        logger.info("Listando todos los equipos")
        return jsonify([equipo.to_dict() for equipo in equipos]), 200
    except Exception as e:
        logger.error(f"Error al obtener equipos: {e}")
        return jsonify({"error": str(e)}), 500

@equipo_bp.route("/equipos/<int:equipo_id>", methods=["GET"])
def get_equipo(equipo_id):
    """Obtener un equipo específico por ID"""
    try:
        equipo = Equipo.query.get_or_404(equipo_id)
        logger.info(f"Obteniendo detalles del equipo {equipo_id}")
        return jsonify(equipo.to_dict()), 200
    except Exception as e:
        logger.error(f"Error al obtener equipo {equipo_id}: {e}")
        return jsonify({"error": str(e)}), 500

@equipo_bp.route("/equipos", methods=["POST"])
def create_equipo():
    """Crear un nuevo equipo"""
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        if not data or "nombre" not in data:
            logger.warning("Intento de creación de equipo fallido: falta el nombre")
            return jsonify({"error": "El nombre del equipo es requerido"}), 400
        
        nuevo_equipo = Equipo(
            nombre=data["nombre"],
            estado=data.get("estado", "Activo"),
            ubicacion_lat=data.get("ubicacion_lat"),
            ubicacion_lng=data.get("ubicacion_lng"),
            fecha_ultima_revision=datetime.strptime(data["fecha_ultima_revision"], "%Y-%m-%d").date() if data.get("fecha_ultima_revision") else None
        )
        
        db.session.add(nuevo_equipo)
        db.session.commit()
        logger.info(f"Equipo {nuevo_equipo.nombre} creado exitosamente")
        
        return jsonify(nuevo_equipo.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error al crear equipo: {e}")
        return jsonify({"error": str(e)}), 500

@equipo_bp.route("/equipos/<int:equipo_id>", methods=["PUT"])
def update_equipo(equipo_id):
    """Actualizar un equipo existente"""
    try:
        equipo = Equipo.query.get_or_404(equipo_id)
        data = request.get_json()
        
        if not data:
            logger.warning(f"Intento de actualización de equipo {equipo_id} fallido: no se proporcionaron datos")
            return jsonify({"error": "No se proporcionaron datos para actualizar"}), 400
        
        # Actualizar campos si están presentes en los datos
        if "nombre" in data:
            equipo.nombre = data["nombre"]
        if "estado" in data:
            equipo.estado = data["estado"]
        if "ubicacion_lat" in data:
            equipo.ubicacion_lat = data["ubicacion_lat"]
        if "ubicacion_lng" in data:
            equipo.ubicacion_lng = data["ubicacion_lng"]
        if "fecha_ultima_revision" in data:
            equipo.fecha_ultima_revision = datetime.strptime(data["fecha_ultima_revision"], "%Y-%m-%d").date() if data["fecha_ultima_revision"] else None
        
        equipo.fecha_actualizacion = datetime.utcnow()
        
        db.session.commit()
        logger.info(f"Equipo {equipo_id} actualizado exitosamente")
        
        return jsonify(equipo.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error al actualizar equipo {equipo_id}: {e}")
        return jsonify({"error": str(e)}), 500

@equipo_bp.route("/equipos/<int:equipo_id>", methods=["DELETE"])
def delete_equipo(equipo_id):
    """Eliminar un equipo"""
    try:
        equipo = Equipo.query.get_or_404(equipo_id)
        db.session.delete(equipo)
        db.session.commit()
        logger.info(f"Equipo {equipo_id} eliminado exitosamente")
        
        return jsonify({"message": "Equipo eliminado exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error al eliminar equipo {equipo_id}: {e}")
        return jsonify({"error": str(e)}), 500

@equipo_bp.route("/equipos/<int:equipo_id>/status", methods=["POST"])
def update_equipo_status(equipo_id):
    """Actualizar el estado y ubicación de un equipo (para datos de monitoreo)"""
    try:
        equipo = Equipo.query.get_or_404(equipo_id)
        data = request.get_json()
        
        if not data:
            logger.warning(f"Intento de actualización de estado de equipo {equipo_id} fallido: no se proporcionaron datos")
            return jsonify({"error": "No se proporcionaron datos de estado"}), 400
        
        # Actualizar estado y ubicación
        if "estado" in data:
            equipo.estado = data["estado"]
        if "ubicacion_lat" in data:
            equipo.ubicacion_lat = data["ubicacion_lat"]
        if "ubicacion_lng" in data:
            equipo.ubicacion_lng = data["ubicacion_lng"]
        
        equipo.fecha_actualizacion = datetime.utcnow()
        
        db.session.commit()
        logger.info(f"Estado y ubicación del equipo {equipo_id} actualizados exitosamente")
        
        return jsonify(equipo.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error al actualizar estado del equipo {equipo_id}: {e}")
        return jsonify({"error": str(e)}), 500


