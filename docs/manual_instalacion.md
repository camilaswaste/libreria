Manual de Instalación - Sistema LIBRERIA EL GRAN POETA

1. Requisitos del Sistema
1.1 Hardware recomendado
1.2 Software necesario
2. Preparación del Entorno
2.1 Instalación de Python
2.2 Configuración del entorno virtual
2.3 Instalación de dependencias
3. Configuración de la Base de Datos
3.1 Instalación de PostgreSQL
3.2 Creación de la base de datos
4. Configuración del Proyecto
4.1 Clonación del repositorio
4.2 Configuración de variables de entorno
4.3 Aplicación de migraciones
5. Inicialización del Sistema
5.1 Creación de superusuario
5.2 Carga de datos iniciales
6. Despliegue
6.1 Configuración del servidor web (Gunicorn)
6.2 Configuración de Nginx (opcional)
7. Verificación de la Instalación
7.1 Pruebas post-instalación
7.2 Solución de problemas comunes


Ahora, desarrollaremos en detalle las secciones 1 y 2 como ejemplo:

1. Requisitos del Sistema


1.1 Hardware recomendado

- Procesador: 2 GHz o superior (se recomienda 4 núcleos o más)
- Memoria RAM: Mínimo 4 GB (se recomienda 8 GB o más)
- Espacio en disco: Mínimo 10 GB de espacio libre


1.2 Software necesario

- Sistema Operativo: Ubuntu 20.04 LTS o superior (también compatible con otras distribuciones Linux, macOS, y Windows)
- Python: Versión 3.8 o superior
- PostgreSQL: Versión 12 o superior
- Git: Última versión estable


2. Preparación del Entorno


2.1 Instalación de Python

1. Abra una terminal.
2. Actualice el índice de paquetes:


sudo apt update



3. Instale Python y pip:


sudo apt install python3 python3-pip



4. Verifique la instalación:


python3 --version
pip3 --version




2.2 Configuración del entorno virtual

1. Instale virtualenv:


pip3 install virtualenv



2. Navegue al directorio donde desea crear el proyecto:


cd /ruta/a/su/proyecto



3. Cree un nuevo entorno virtual:


python3 -m venv libreria_env



4. Active el entorno virtual:


source libreria_env/bin/activate





2.3 Instalación de dependencias

1. Asegúrese de que el entorno virtual esté activado.
2. Instale las dependencias del proyecto utilizando el archivo requirements.txt:

pip install -r requirements.txt



3. Verifique que todas las dependencias se hayan instalado correctamente:

pip list



Nota: Si encuentra algún error durante la instalación de dependencias, asegúrese de tener instaladas las bibliotecas de desarrollo necesarias. Puede instalarlas con:


sudo apt install python3-dev libpq-dev
