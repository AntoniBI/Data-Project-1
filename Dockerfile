# Usar la imagen base de NiFi
FROM apache/nifi:1.28.1

# Cambiar a usuario root para modificar archivos
USER root

# Copiar el archivo flow.xml.gz al directorio de configuración de NiFi
COPY ./nifi-config/flow.xml.gz /opt/nifi/nifi-current/conf/flow.xml.gz

# Modificar el archivo nifi.properties para incluir las configuraciones necesarias
RUN sed -i 's|^nifi.flow.configuration.file=.*|nifi.flow.configuration.file=./conf/flow.xml.gz|' /opt/nifi/nifi-current/conf/nifi.properties && \
    sed -i 's|^nifi.flowcontroller.autoResumeState=.*|nifi.flowcontroller.autoResumeState=true|' /opt/nifi/nifi-current/conf/nifi.properties && \
    sed -i 's|^nifi.sensitive.props.key=.*|nifi.sensitive.props.key=GR6MYZhdJsfir8HWnPrphMo2U6w4zAyb|' /opt/nifi/nifi-current/conf/nifi.properties

# Opcional: cambiar permisos si es necesario
RUN chown -R nifi:nifi /opt/nifi/nifi-current/conf/flow.xml.gz

# Regresar al usuario original de NiFi
USER nifi

# Iniciar NiFi
CMD ["bin/nifi.sh", "run"]
