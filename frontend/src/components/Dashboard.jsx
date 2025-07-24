import { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Truck, MapPin, Settings, LogOut, Plus } from 'lucide-react';
import axios from 'axios';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// Fix para los iconos de Leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

const Dashboard = ({ user, onLogout }) => {
  const [equipos, setEquipos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedEquipo, setSelectedEquipo] = useState(null);

  useEffect(() => {
    fetchEquipos();
  }, []);

  const fetchEquipos = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('/api/equipos', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      setEquipos(response.data);
    } catch (err) {
      setError('Error al cargar los equipos');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const getEstadoColor = (estado) => {
    switch (estado) {
      case 'Activo':
        return 'bg-green-500';
      case 'Inactivo':
        return 'bg-red-500';
      case 'En mantenimiento':
        return 'bg-yellow-500';
      default:
        return 'bg-gray-500';
    }
  };

  const getEstadoBadgeVariant = (estado) => {
    switch (estado) {
      case 'Activo':
        return 'default';
      case 'Inactivo':
        return 'destructive';
      case 'En mantenimiento':
        return 'secondary';
      default:
        return 'outline';
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    onLogout();
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Cargando dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-3">
              <Truck className="h-8 w-8 text-blue-600" />
              <h1 className="text-2xl font-bold text-gray-900">
                Monitoreo de Equipos Pesados
              </h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-600">
                Bienvenido, {user.nombre}
              </span>
              <Button variant="outline" size="sm" onClick={handleLogout}>
                <LogOut className="h-4 w-4 mr-2" />
                Salir
              </Button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {error && (
          <Alert variant="destructive" className="mb-6">
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        {/* Estadísticas */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Equipos</CardTitle>
              <Truck className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{equipos.length}</div>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Equipos Activos</CardTitle>
              <div className="h-4 w-4 bg-green-500 rounded-full"></div>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {equipos.filter(e => e.estado === 'Activo').length}
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">En Mantenimiento</CardTitle>
              <Settings className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {equipos.filter(e => e.estado === 'En mantenimiento').length}
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Mapa */}
          <Card className="lg:col-span-1">
            <CardHeader>
              <CardTitle className="flex items-center">
                <MapPin className="h-5 w-5 mr-2" />
                Ubicación de Equipos
              </CardTitle>
              <CardDescription>
                Visualización en tiempo real de la ubicación de todos los equipos
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="h-96 rounded-lg overflow-hidden">
                <MapContainer
                  center={[18.4861, -69.9312]} // Santo Domingo, RD
                  zoom={10}
                  style={{ height: '100%', width: '100%' }}
                >
                  <TileLayer
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                  />
                  {equipos.filter(equipo => equipo.ubicacion_lat && equipo.ubicacion_lng).map(equipo => (
                    <Marker
                      key={equipo.id}
                      position={[equipo.ubicacion_lat, equipo.ubicacion_lng]}
                    >
                      <Popup>
                        <div className="p-2">
                          <h3 className="font-semibold">{equipo.nombre}</h3>
                          <p className="text-sm text-gray-600">Estado: {equipo.estado}</p>
                          {equipo.fecha_ultima_revision && (
                            <p className="text-xs text-gray-500">
                              Última revisión: {new Date(equipo.fecha_ultima_revision).toLocaleDateString()}
                            </p>
                          )}
                        </div>
                      </Popup>
                    </Marker>
                  ))}
                </MapContainer>
              </div>
            </CardContent>
          </Card>

          {/* Lista de Equipos */}
          <Card>
            <CardHeader>
              <div className="flex justify-between items-center">
                <div>
                  <CardTitle>Lista de Equipos</CardTitle>
                  <CardDescription>
                    Estado actual de todos los equipos registrados
                  </CardDescription>
                </div>
                <Button size="sm">
                  <Plus className="h-4 w-4 mr-2" />
                  Agregar
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-4 max-h-96 overflow-y-auto">
                {equipos.length === 0 ? (
                  <div className="text-center py-8 text-gray-500">
                    <Truck className="h-12 w-12 mx-auto mb-4 text-gray-300" />
                    <p>No hay equipos registrados</p>
                  </div>
                ) : (
                  equipos.map(equipo => (
                    <div
                      key={equipo.id}
                      className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50 cursor-pointer"
                      onClick={() => setSelectedEquipo(equipo)}
                    >
                      <div className="flex items-center space-x-3">
                        <div className={`h-3 w-3 rounded-full ${getEstadoColor(equipo.estado)}`}></div>
                        <div>
                          <h3 className="font-medium">{equipo.nombre}</h3>
                          <p className="text-sm text-gray-500">
                            {equipo.ubicacion_lat && equipo.ubicacion_lng
                              ? `${equipo.ubicacion_lat.toFixed(4)}, ${equipo.ubicacion_lng.toFixed(4)}`
                              : 'Ubicación no disponible'
                            }
                          </p>
                        </div>
                      </div>
                      <Badge variant={getEstadoBadgeVariant(equipo.estado)}>
                        {equipo.estado}
                      </Badge>
                    </div>
                  ))
                )}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

