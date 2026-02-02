Proyecto Productos y Órdenes

Docker + Kubernetes (Minikube) – Windows

Proyecto académico de Sistemas Distribuidos que implementa una arquitectura de microservicios con:

Servicio de Productos

Servicio de Órdenes

Frontend web

Bases de datos PostgreSQL independientes

Docker y Kubernetes (Minikube)

⚠️ Nota importante:
Para el entorno académico se utiliza NodePort y port-forward.
No se usa Ingress ni túneles, para mantener la solución simple y evaluable en laboratorio/examen.

🖥️ Requisitos (Windows)

Docker Desktop (en ejecución)

kubectl

Minikube

PowerShell

(Opcional) Git

Cuenta en Docker Hub (para subir imágenes)

🅰️ A) Ejecutar con Docker Compose (LOCAL)
1️⃣ Levantar todo

Desde la raíz del proyecto:

docker compose up --build

2️⃣ URLs disponibles

Frontend:
👉 http://localhost:8080

Servicio Productos (Swagger):
👉 http://localhost:8000/docs

Servicio Órdenes (Swagger):
👉 http://localhost:8001/docs

3️⃣ Detener contenedores
docker compose down

4️⃣ Detener y borrar volúmenes (BORRA BASES DE DATOS)
docker compose down -v

☸️ B) Ejecutar con Kubernetes (Minikube)
1️⃣ Arrancar Minikube
minikube start --driver=docker


Verificar:

minikube status
kubectl get nodes

2️⃣ Usar Docker interno de Minikube

⚠️ Obligatorio antes de construir imágenes

minikube -p minikube docker-env | Invoke-Expression


Verifica:

docker images

3️⃣ Construir imágenes Docker

Desde la raíz del proyecto:

docker build -t servicio-productos:1.0 .\servicio-productos
docker build -t servicio-ordenes:1.0 .\servicio-ordenes
docker build -t frontend:1.0 .\frontend

4️⃣ Aplicar manifiestos Kubernetes
kubectl apply -f .\k8s\00-namespace.yml
kubectl apply -f .\k8s\01-configmaps.yml
kubectl apply -f .\k8s\02-postgres-productos.yml
kubectl apply -f .\k8s\03-postgres-ordenes.yml
kubectl apply -f .\k8s\04-servicio-productos.yml
kubectl apply -f .\k8s\05-servicio-ordenes.yml
kubectl apply -f .\k8s\06-frontend.yml

5️⃣ Ver estado del sistema
kubectl get pods -n tienda
kubectl get svc  -n tienda


Logs:

kubectl logs -n tienda deploy/servicio-productos
kubectl logs -n tienda deploy/servicio-ordenes
kubectl logs -n tienda deploy/frontend

6️⃣ Exponer APIs con port-forward (OBLIGATORIO)
Terminal 1 – Productos
kubectl port-forward -n tienda svc/servicio-productos 8000:8000

Terminal 2 – Órdenes
kubectl port-forward -n tienda svc/servicio-ordenes 8001:8001


⚠️ No cerrar estas terminales

7️⃣ Abrir el frontend
minikube service -n tienda frontend


👉 Se abrirá automáticamente el navegador.

8️⃣ Probar APIs manualmente (opcional)

Productos:
👉 http://localhost:8000/docs

Órdenes:
👉 http://localhost:8001/docs

9️⃣ Eliminar todo el entorno Kubernetes
kubectl delete ns tienda

🔟 Apagar Minikube
minikube stop


Eliminar completamente el clúster:

minikube delete

🚀 Subir imágenes a Docker Hub
1️⃣ Iniciar sesión
docker login

2️⃣ Etiquetar imágenes

(Reemplaza TU_USUARIO por tu usuario de Docker Hub)

docker tag servicio-productos:1.0 TU_USUARIO/servicio-productos:1.0
docker tag servicio-ordenes:1.0  TU_USUARIO/servicio-ordenes:1.0
docker tag frontend:1.0          TU_USUARIO/frontend:1.0

3️⃣ Subir imágenes
docker push TU_USUARIO/servicio-productos:1.0
docker push TU_USUARIO/servicio-ordenes:1.0
docker push TU_USUARIO/frontend:1.0

📝 Notas importantes

El servicio de Órdenes consulta al servicio de Productos y descuenta stock.

Cada microservicio usa su base de datos PostgreSQL independiente.

El frontend consume los servicios vía NodePort + port-forward.

En producción se recomienda:

Ingress

LoadBalancer

Secrets gestionados

Persistencia con PVC

CORS restringido

⚡ Resumen rápido (para el examen)
minikube start --driver=docker
minikube -p minikube docker-env | Invoke-Expression

docker build -t servicio-productos:1.0 .\servicio-productos
docker build -t servicio-ordenes:1.0 .\servicio-ordenes
docker build -t frontend:1.0 .\frontend

kubectl apply -f k8s/
kubectl port-forward -n tienda svc/servicio-productos 8000:8000
kubectl port-forward -n tienda svc/servicio-ordenes 8001:8001

minikube service -n tienda frontend