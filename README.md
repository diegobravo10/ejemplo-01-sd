#  Proyecto Productos y Órdenes  
### Docker + Kubernetes (Minikube) – Windows

---

## A) Ejecutar con Docker Compose (LOCAL)

### Levantar todo
Desde la raíz del proyecto:
```
docker compose up --build
```
### URLs disponibles

Frontend
 http://localhost:8080

Servicio Productos (Swagger)
 http://localhost:8000/docs

Servicio Órdenes (Swagger)
 http://localhost:8001/docs

### Detener contenedores
```
docker compose down
```
### Detener y borrar volúmenes
```
docker compose down -v
```
## B) Ejecutar con Kubernetes (Minikube)
### Arrancar Minikube
```
minikube start --driver=docker
```
Verificar:
```
minikube status
```
```
kubectl get nodes
```
### Usar Docker interno de Minikube
```
minikube -p minikube docker-env | Invoke-Expression
```
Verificar:
```
docker images
```
### Construir imágenes Docker
Desde la raíz del proyecto:
```
docker build -t servicio-productos:1.0 .\servicio-productos
docker build -t servicio-ordenes:1.0 .\servicio-ordenes
docker build -t frontend:1.0 .\frontend
```
### Aplicar manifiestos Kubernetes
```
kubectl apply -f .\k8s\00-namespace.yml
kubectl apply -f .\k8s\01-configmaps.yml
kubectl apply -f .\k8s\02-postgres-productos.yml
kubectl apply -f .\k8s\03-postgres-ordenes.yml
kubectl apply -f .\k8s\04-servicio-productos.yml
kubectl apply -f .\k8s\05-servicio-ordenes.yml
kubectl apply -f .\k8s\06-frontend.yml
```
### Ver estado del sistema
```
kubectl get pods -n tienda
kubectl get svc  -n tienda
```
Logs:
```
kubectl logs -n tienda deploy/servicio-productos
kubectl logs -n tienda deploy/servicio-ordenes
kubectl logs -n tienda deploy/frontend
```
### Exponer APIs con port-forward
Terminal 1 – Productos
```
kubectl port-forward -n tienda svc/servicio-productos 8000:8000
```
Terminal 2 – Órdenes
```
kubectl port-forward -n tienda svc/servicio-ordenes 8001:8001
```

### Abrir el frontend
```
minikube service -n tienda frontend
```

### Probar APIs manualmente (opcional)
Productos
```
http://localhost:8000/docs
```
Órdenes
```
http://localhost:8001/docs
```

### Eliminar todo el entorno Kubernetes
```
kubectl delete ns tienda
```
### Apagar Minikube
```
minikube stop
```
Eliminar completamente el clúster:
```
minikube delete
```
## Subir imágenes a Docker Hub
### Iniciar sesión
```
docker login
```
### Etiquetar imágenes
(Reemplaza TU_USUARIO por tu usuario de Docker Hub)
```
docker tag servicio-productos:1.0 TU_USUARIO/servicio-productos:1.0
docker tag servicio-ordenes:1.0  TU_USUARIO/servicio-ordenes:1.0
docker tag frontend:1.0          TU_USUARIO/frontend:1.0
```
### Subir imágenes
```
docker push TU_USUARIO/servicio-productos:1.0
docker push TU_USUARIO/servicio-ordenes:1.0
docker push TU_USUARIO/frontend:1.0
```

## Resumen rápido
```
minikube start --driver=docker
minikube -p minikube docker-env | Invoke-Expression

docker build -t servicio-productos:1.0 .\servicio-productos
docker build -t servicio-ordenes:1.0 .\servicio-ordenes
docker build -t frontend:1.0 .\frontend

kubectl apply -f k8s/
kubectl port-forward -n tienda svc/servicio-productos 8000:8000
kubectl port-forward -n tienda svc/servicio-ordenes 8001:8001

minikube service -n tienda frontend
```
