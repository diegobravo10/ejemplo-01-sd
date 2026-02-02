# Kubernetes + Minikube (Windows / PowerShell)
## MINIKUBE — Gestión del clúster
### Iniciar Minikube
```
minikube start --driver=docker
```
### Detener Minikube
```
minikube stop
```
### Eliminar clúster
```
minikube delete
```
### Ver estado
```
minikube status
```
### Ver IP de Minikube
```
minikube ip
```
## Docker interno de Minikube
### Usar Docker de Minikube
```
minikube -p minikube docker-env | Invoke-Expression
```
### Ver imágenes
```
docker images
```
## KUBECTL — Información general
### Ver contexto actual
```
kubectl config current-context
```
### Ver nodos
```
kubectl get nodes
```
### Ver namespaces
```
kubectl get ns
```
### Crear namespace
```
kubectl create ns tienda
```
## RECURSOS — Ver estado
### Ver Pods
```
kubectl get pods
kubectl get pods -n tienda
```
### Ver Deployments
```
kubectl get deployments -n tienda
```
### Ver Services
```
kubectl get svc -n tienda
```
### Ver todo
```
kubectl get all -n tienda
```
## LOGS y DEBUG
### Ver logs de un Pod
```
kubectl logs POD_NAME -n tienda
```
### Logs de un Deployment
```
kubectl logs deploy/servicio-productos -n tienda
```
### Logs en tiempo real
```
kubectl logs -f POD_NAME -n tienda
```
## INSPECCIÓN (MUY IMPORTANTE)
### Ver detalles de un recurso
```
kubectl describe pod POD_NAME -n tienda
kubectl describe deployment servicio-productos -n tienda
kubectl describe svc servicio-productos -n tienda
```
## APLICAR / BORRAR YAML
### Aplicar un archivo
```
kubectl apply -f archivo.yml
```
### Aplicar una carpeta completa
```
kubectl apply -f k8s/
```
### Borrar un recurso
```
kubectl delete -f archivo.yml
```
### Borrar namespace (BORRA TODO)
```
kubectl delete ns tienda
```
## ESCALADO DE SERVICIOS
### Escalar a N instancias
```
kubectl scale deployment servicio-productos --replicas=3 -n tienda
```
### Volver a 1
```
kubectl scale deployment servicio-productos --replicas=1 -n tienda
```
## EXPONER SERVICIOS

### Port-forward
```
kubectl port-forward -n tienda svc/servicio-productos 8000:8000
```
### Abrir servicio NodePort
```
minikube service -n tienda frontend
```
## REINICIAR / ACTUALIZAR
### Reiniciar un Deployment
```
kubectl rollout restart deployment servicio-productos -n tienda
```
### Ver historial
```
kubectl rollout history deployment servicio-productos -n tienda
```
## CONFIGURACIÓN
### Ver ConfigMaps
```
kubectl get configmap -n tienda
```
### Ver Secrets
```
kubectl get secrets -n tienda
```
## DASHBOARD DE KUBERNETES ( MUY IMPORTANTE)
### Habilitar dashboard
```
minikube dashboard
```

Esto: abre el navegador

muestra Pods, Services, Deployments

 No cierres la terminal

## AUTOSCALING (OPCIONAL)
### Habilitar métricas
```
minikube addons enable metrics-server
```
### Crear HPA
```
kubectl autoscale deployment servicio-productos \
  --cpu-percent=50 \
  --min=1 \
  --max=5 \
  -n tienda
```
### Ver HPA
```
kubectl get hpa -n tienda
```
## TEST DE CONECTIVIDAD
### Entrar a un Pod
```
kubectl exec -it POD_NAME -n tienda -- sh
```
## COMANDOS CLAVE PARA EL EXAMEN
```
minikube start
kubectl get pods -n tienda
kubectl get svc -n tienda
kubectl scale deployment servicio-productos --replicas=3 -n tienda
kubectl port-forward -n tienda svc/servicio-productos 8000:8000
minikube dashboard
```
