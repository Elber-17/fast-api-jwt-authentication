## Ejecutar Api Con Docker
### Pre - Requisitos
```
Tener instalado docker y docker-compose
Tener corriendo la base de datos y odoo en docker
```
### Verificación de Requisitos
##### - Verificación de Instalacion de Docker
```
docker -v 
```
##### - Verificación de Instalacion de Docker-Compose
```
docker-compose -v
```
##### - Verificación de Contenedores de Odoo y Postgress
```
docker ps
```
##### -Ejemplo de Salida
```
CONTAINER ID 		IMAGE		COMMAND								CREATED				STATUS
47264a277a41		crm_web		"/usr/bin/odoo -c /e…"			About an hour ago	Up About an hour
85e1cfc0d3b8		postgres:12	"docker-entrypoint.s…"			About an hour ago	Up About an hour
```
### Correr Contenedor Con La Api 
```
docker ps
```
##### -Construir la Imagen de la api
```
docker build -t crm-api .
```
##### -Correr contenedor con la imagen creada
```
docker run -p 8000:8000 --name crm-api crm-api
```
### Conectar el contenedor de la api a la network de odoo
##### -Ver lista de redes de docker
```
docker network ls
```
##### -Ejemplo de Salida
```
NETWORK ID		 NAME                    DRIVER    SCOPE
6d4165f70f29		 bridge                        bridge    local
9af344957cb7		crm_docker-service   bridge    local
950ad4302571	   host                           host       local
c4b9fc485f79		 none                          null         local

```
##### -Conectar el contenedor de la api a la Red
```
docker network connect crm_docker-service crm-api
```

##### Para crear la base de datos sqlite de usuarios con permiso para crear api-keys

alembic upgrade head

