# Docker Blender & CDK - Brender Studio

## Descripcion
Este repositorio contiene la logica de Blender y CDK para renderizar un archivo `.blend` en un contenedor de Docker.
Toda la infraestructura esta en la carpeta `aws_cdk` y la logica de docker en la carpeta `docker_blender`.


## Codebuild

En una tarea de codebuild usaremos el archivo `buildspec.yml` para construir la imagen de docker y subirla a ECR. Seguido de esto, crearemos un stack de CDK para desplegar la infraestructura necesaria para renderizar el archivo .blend en un contenedor de Docker.
