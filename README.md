# Sistema de Monitoreo de Equipos Pesados

## Descripción General

El Sistema de Monitoreo de Equipos Pesados es una aplicación web completa diseñada para gestionar y monitorear vehículos y maquinaria pesada en tiempo real. La aplicación proporciona una interfaz intuitiva para el seguimiento de ubicación, estado operacional, mantenimiento y análisis de rendimiento de equipos industriales.

## Características Principales

### 🚛 Gestión de Equipos
- Registro y catalogación de equipos pesados
- Seguimiento de estado operacional (Activo, Inactivo, En mantenimiento)
- Historial de mantenimiento y revisiones
- Información técnica detallada de cada equipo

### 📍 Monitoreo de Ubicación
- Visualización en mapa interactivo con Leaflet
- Seguimiento GPS en tiempo real
- Geolocalización precisa de equipos
- Rutas y trayectorias históricas

### 👥 Sistema de Usuarios
- Autenticación segura con JWT
- Roles y permisos diferenciados
- Panel de administración
- Gestión de sesiones

### 📊 Dashboard y Reportes
- Panel de control con métricas clave
- Estadísticas de rendimiento
- Alertas y notificaciones
- Reportes personalizables

## Arquitectura Técnica

### Backend (Flask)
- **Framework**: Flask con Python 3.11
- **Base de Datos**: SQLite con SQLAlchemy ORM
- **Autenticación**: JWT (JSON Web Tokens)
- **API**: RESTful con endpoints documentados

### Frontend (React)
- **Framework**: React 18 con Vite
- **Mapas**: Leaflet para visualización geográfica
- **Estilos**: Tailwind CSS para diseño responsivo
- **Estado**: Context API para gestión de estado

### Estructura del Proyecto

```
monitoreo-equipos-app/
├── backend/
│   ├── src/
│   │   ├── models/
│   │   │   ├── user.py          # Modelo de usuarios
│   │   │   └── equipo.py        # Modelo de equipos
│   │   ├── routes/
│   │   │   ├── user.py          # Rutas de usuarios
│   │   │   └── equipo.py        # Rutas de equipos
│   │   └── main.py              # Aplicación principal
│   ├── requirements.txt         # Dependencias Python
│   └── create_sample_data.py    # Script de datos de ejemplo
└── frontend/
    ├── src/
    │   ├── components/
    │   │   ├── Login.jsx        # Componente de login
    │   │   └── Dashboard.jsx    # Panel principal
    │   └── App.jsx              # Componente raíz
    └── package.json             # Dependencias Node.js
```

## Instalación y Configuración

### Prerrequisitos
- Python 3.11+
- Node.js 20+
- npm o pnpm

### Configuración del Backend

1. **Crear entorno virtual**:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows
```

2. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

3. **Crear datos de ejemplo**:
```bash
python create_sample_data.py
```

4. **Ejecutar servidor**:
```bash
python src/main.py
```

### Configuración del Frontend

1. **Instalar dependencias**:
```bash
cd frontend
pnpm install
```

2. **Ejecutar servidor de desarrollo**:
```bash
pnpm run dev
```

## Uso de la Aplicación

### Credenciales de Acceso
- **Email**: admin@test.com
- **Contraseña**: admin123

### Funcionalidades Disponibles

#### Panel de Control
El dashboard principal muestra:
- Resumen de equipos por estado
- Mapa interactivo con ubicaciones
- Estadísticas de mantenimiento
- Alertas y notificaciones

#### Gestión de Equipos
- **Agregar Equipo**: Formulario para registrar nuevos equipos
- **Editar Información**: Actualizar datos técnicos y estado
- **Historial**: Visualizar registros de mantenimiento
- **Ubicación**: Seguimiento GPS en tiempo real

#### Monitoreo en Mapa
- Visualización de todos los equipos en mapa interactivo
- Filtros por estado y tipo de equipo
- Información detallada al hacer clic en marcadores
- Rutas y trayectorias históricas

## API Endpoints

### Autenticación
- `POST /api/login` - Iniciar sesión
- `POST /api/register` - Registrar usuario
- `POST /api/verify-token` - Verificar token JWT

### Equipos
- `GET /api/equipos` - Listar todos los equipos
- `POST /api/equipos` - Crear nuevo equipo
- `GET /api/equipos/<id>` - Obtener equipo específico
- `PUT /api/equipos/<id>` - Actualizar equipo
- `DELETE /api/equipos/<id>` - Eliminar equipo

### Usuarios
- `GET /api/users` - Listar usuarios (admin)
- `GET /api/users/<id>` - Obtener usuario específico
- `PUT /api/users/<id>` - Actualizar usuario

## Datos de Ejemplo

La aplicación incluye equipos de ejemplo:

| Equipo | Estado | Ubicación | Última Revisión |
|--------|--------|-----------|-----------------|
| Excavadora CAT 320 | Activo | Santo Domingo | 01/12/2024 |
| Bulldozer D6T | En mantenimiento | Santiago | 15/11/2024 |
| Grúa Liebherr LTM 1050 | Activo | Puerto Plata | 10/12/2024 |
| Camión Volvo FMX | Inactivo | La Romana | 20/10/2024 |
| Retroexcavadora JCB 3CX | Activo | San Pedro | 05/12/2024 |

## Tecnologías Utilizadas

### Backend
- **Flask**: Framework web ligero y flexible
- **SQLAlchemy**: ORM para manejo de base de datos
- **Flask-JWT-Extended**: Autenticación con tokens JWT
- **Flask-CORS**: Manejo de CORS para API
- **Werkzeug**: Utilidades WSGI y hashing de contraseñas

### Frontend
- **React**: Biblioteca para interfaces de usuario
- **Vite**: Herramienta de construcción rápida
- **Leaflet**: Biblioteca de mapas interactivos
- **Axios**: Cliente HTTP para API calls
- **Tailwind CSS**: Framework de estilos utilitarios

## Próximas Mejoras

### Funcionalidades Planificadas
1. **Notificaciones Push**: Alertas en tiempo real
2. **Reportes Avanzados**: Análisis de rendimiento y costos
3. **Integración IoT**: Sensores para monitoreo automático
4. **App Móvil**: Aplicación nativa para dispositivos móviles
5. **Geofencing**: Alertas por zonas geográficas
6. **Mantenimiento Predictivo**: IA para predicción de fallas

### Mejoras Técnicas
1. **Base de Datos**: Migración a PostgreSQL para producción
2. **Autenticación**: Integración con OAuth2 y SSO
3. **Caching**: Redis para optimización de rendimiento
4. **Monitoreo**: Logging y métricas con Prometheus
5. **Despliegue**: Containerización con Docker
6. **Testing**: Cobertura completa de pruebas unitarias

## Contribución

Para contribuir al proyecto:

1. Fork el repositorio
2. Crear rama de feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Soporte

Para soporte técnico o consultas:
- **Email**: soporte@monitoreo-equipos.com
- **Documentación**: [Wiki del proyecto](https://github.com/erickherndza/monitoreo-equipos/wiki)
- **Issues**: [GitHub Issues](https://github.com/erickherndza/monitoreo-equipos/issues)

---

**Desarrollado por**: Manus AI  
**Versión**: 1.0.0  
**Fecha**: Julio 2025

