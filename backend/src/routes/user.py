import logging
from flask import Blueprint, request, jsonify
from src.models.user import User, db
import jwt
from datetime import datetime, timedelta
import os

user_bp = Blueprint('user', __name__)

logger = logging.getLogger(__name__)

# Clave secreta para JWT (en producción debería estar en variables de entorno)
JWT_SECRET = os.environ.get('JWT_SECRET', 'tu-clave-secreta-super-segura')

def generate_token(user_id):
    """Generar token JWT para el usuario"""
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=24)  # Token válido por 24 horas
    }
    return jwt.encode(payload, JWT_SECRET, algorithm='HS256')

def verify_token(token):
    """Verificar y decodificar token JWT"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        logger.warning('Token expirado')
        return None
    except jwt.InvalidTokenError:
        logger.warning('Token inválido')
        return None

@user_bp.route('/login', methods=['POST'])
def login():
    """Autenticación de usuario"""
    try:
        data = request.get_json()
        
        if not data or 'email' not in data or 'password' not in data:
            logger.warning('Intento de login fallido: faltan credenciales (email o password)')
            return jsonify({'error': 'Email y contraseña son requeridos'}), 400
        
        user = User.query.filter_by(email=data['email']).first()
        
        if user and user.check_password(data['password']) and user.activo:
            token = generate_token(user.id)
            logger.info(f'Usuario {user.email} ha iniciado sesión exitosamente')
            return jsonify({
                'token': token,
                'user': user.to_dict()
            }), 200
        else:
            logger.warning(f'Intento de login fallido para el email {data["email"]}: credenciales inválidas')
            return jsonify({'error': 'Credenciales inválidas'}), 401
    
    except Exception as e:
        logger.error(f'Error en el login: {e}')
        return jsonify({'error': str(e)}), 500

@user_bp.route('/register', methods=['POST'])
def register():
    """Registro de nuevo usuario"""
    try:
        data = request.get_json()
        
        if not data or 'nombre' not in data or 'email' not in data or 'password' not in data:
            logger.warning('Intento de registro fallido: faltan credenciales (nombre, email o password)')
            return jsonify({'error': 'Nombre, email y contraseña son requeridos'}), 400
        
        # Verificar si el email ya existe
        if User.query.filter_by(email=data['email']).first():
            logger.warning(f'Intento de registro fallido: el email {data["email"]} ya está registrado')
            return jsonify({'error': 'El email ya está registrado'}), 400
        
        # Crear nuevo usuario
        nuevo_usuario = User(
            nombre=data['nombre'],
            email=data['email']
        )
        nuevo_usuario.set_password(data['password'])
        
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        # Generar token para el nuevo usuario
        token = generate_token(nuevo_usuario.id)
        logger.info(f'Usuario {nuevo_usuario.email} registrado exitosamente')
        
        return jsonify({
            'token': token,
            'user': nuevo_usuario.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        logger.error(f'Error en el registro: {e}')
        return jsonify({'error': str(e)}), 500

@user_bp.route('/verify-token', methods=['POST'])
def verify_user_token():
    """Verificar token JWT"""
    try:
        data = request.get_json()
        
        if not data or 'token' not in data:
            logger.warning('Verificación de token fallida: token no proporcionado')
            return jsonify({'error': 'Token es requerido'}), 400
        
        user_id = verify_token(data['token'])
        
        if user_id:
            user = User.query.get(user_id)
            if user and user.activo:
                logger.info(f'Token verificado para el usuario {user.email}')
                return jsonify({
                    'valid': True,
                    'user': user.to_dict()
                }), 200
        logger.warning('Verificación de token fallida: token inválido o usuario inactivo')
        return jsonify({'valid': False}), 401
    
    except Exception as e:
        logger.error(f'Error en la verificación de token: {e}')
        return jsonify({'error': str(e)}), 500

@user_bp.route('/users', methods=['GET'])
def get_users():
    """Obtener todos los usuarios (requiere autenticación)"""
    try:
        # Verificar token en headers
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            logger.warning('Acceso denegado a /users: token de autorización requerido')
            return jsonify({'error': 'Token de autorización requerido'}), 401
        
        token = auth_header.split(' ')[1]
        user_id = verify_token(token)
        
        if not user_id:
            logger.warning('Acceso denegado a /users: token inválido')
            return jsonify({'error': 'Token inválido'}), 401
        
        users = User.query.filter_by(activo=True).all()
        logger.info('Listando todos los usuarios')
        return jsonify([user.to_dict() for user in users]), 200
    
    except Exception as e:
        logger.error(f'Error al obtener usuarios: {e}')
        return jsonify({'error': str(e)}), 500

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        logger.info(f'Obteniendo detalles del usuario {user_id}')
        return jsonify(user.to_dict())
    except Exception as e:
        logger.error(f'Error al obtener usuario {user_id}: {e}')
        return jsonify({'error': str(e)}), 500

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        data = request.json
        user.nombre = data.get('nombre', user.nombre)
        user.email = data.get('email', user.email)
        if 'password' in data:
            user.set_password(data['password'])
        db.session.commit()
        logger.info(f'Usuario {user_id} actualizado exitosamente')
        return jsonify(user.to_dict())
    except Exception as e:
        db.session.rollback()
        logger.error(f'Error al actualizar usuario {user_id}: {e}')
        return jsonify({'error': str(e)}), 500

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        logger.info(f'Usuario {user_id} eliminado exitosamente')
        return '', 204
    except Exception as e:
        db.session.rollback()
        logger.error(f'Error al eliminar usuario {user_id}: {e}')
        return jsonify({'error': str(e)}), 500


