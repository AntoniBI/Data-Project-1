#!/bin/bash

# Inicia los servicios principales
echo "Iniciando servicios principales (nifi, mongo, postgres, etc.)..."
docker-compose up -d nifi mongo mongo-express postgres pgadmin

# Esperar unos segundos para asegurarse de que los servicios estén activos
echo "Esperando que los servicios principales se inicien..."
sleep 10

# Preguntar si quieres iniciar el servicio "back"
read -p "¿Quieres iniciar el servicio 'back'? (Y/N): " start_back
if [[ "$start_back" =~ ^[Yy]$ ]]; then
  echo "Iniciando 'back'..."
  docker-compose up -d back
else
  echo "'back' no se iniciará."
fi

# Preguntar si quieres iniciar el servicio "front"
read -p "¿Quieres iniciar el servicio 'front'? (Y/N): " start_front
if [[ "$start_front" =~ ^[Yy]$ ]]; then
  echo "Iniciando 'front'..."
  docker-compose up -d front
else
  echo "'front' no se iniciará."
fi

echo "¡Listo! Los servicios están configurados según tus elecciones."
