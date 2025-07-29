import os
import sys
import logging
from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from src.models.user import db
from src.routes.user import user_bp
from src.routes.equipo import equipo_bp

# Configuración de logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# DON\'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET_KEY", "asdf#FGSgvasgf$5$WGT")

# Habilitar CORS para todas las rutas
CORS(app)

# Configuración de la base de datos para SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///monitoreo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# Registrar Blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(equipo_bp, url_prefix='/api')

with app.app_context():
    db.create_all()

@app.route('/')
def hello_world():
    return jsonify(message="¡Bienvenido al API de Monitoreo de Equipos Pesados!")

# Ruta para servir el frontend (si está en la misma aplicación Flask)
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


