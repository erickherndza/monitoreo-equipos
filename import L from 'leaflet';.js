import L from 'leaflet';

// Íconos personalizados
const iconos = {
  verde: new L.Icon({
    iconUrl: require('./icons/marker-green.png'),
    shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
  }),
  amarillo: new L.Icon({
    iconUrl: require('./icons/marker-yellow.png'),
    shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
  }),
  rojo: new L.Icon({
    iconUrl: require('./icons/marker-red.png'),
    shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
  })
};

// Función para determinar color de ícono
const obtenerIcono = (item) => {
  if (item.temperatura > 90 || item.combustible < 15) return iconos.rojo;
  if (item.temperatura > 80 || item.combustible < 30) return iconos.amarillo;
  return iconos.verde;
};
