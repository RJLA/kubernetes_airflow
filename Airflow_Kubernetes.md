# Acessing Airflow UI via Kubernetes

## Requirements
- Kubectl
- Helm
- Docker
- KinD
#### Please note that these requirements are also need to install first before proceeding to airflow.

> minikube start

## 1. Create namespace for airflow
> kubectl create namespace xops-airflow

## 2. Create a configmap for dags.yaml

>kubectl apply -f dags.yaml

## 3. Add a new repo to helm
> helm repo add xops-airflow-repo  https://charts.bitnami.com/bitnami  -n xops-airflow

> helm repo update -n xops-airflow

## 4. Install helm 
> helm install xops-airflow-release xops-airflow-repo/airflow -n xops-airflow

## 4. Edit the values.yaml
>  helm fetch xops-airflow-repo/airflow --untar

>  cd airflow
## values.yaml template
```
ingress:
  enabled: True
  ingressClassName: "nginx"
  pathType: ImplementationSpecific
  apiVersion: ""
  hostname: "localhost"
  executor: KubernetesExecutor
  extraEnvVars:
    - name: "AIRFLOW__API__ENABLE_EXPERIMENTAL_API"
      value: "True"
    - name: "AIRFLOW__API__AUTH_BACKEND"
      value: "airflow.api.auth.backend.basic_auth"

postgresql:
  enabled: true
  auth:
    username: bn_airflow
    password: ""
    database: bitnami_airflow

redis:
  enabled: true
  auth:
    enabled: true
    password: "password"

auth:
  username: "admin"
  password: "admin"
dags:
  existingConfigmap: "airflowdag1"
```

>  helm upgrade --install xops-airflow-release -f values.yaml xops-airflow-repo/airflow -n xops-airflow

## retreive password

```
export AIRFLOW_PASSWORD=$(kubectl get secret --namespace "xops-airflow" xops-airflow-release -o jsonpath="{.data.airflow-password}" | base64 -d)
    echo User:     admin
    echo Password: $AIRFLOW_PASSWORD
```

##  5. check services
> kubectl get services -n xops-airflow

## 6. Forward traffic to port 8080 using the service that listens to port 8080
> kubectl port-forward svc/xops-airflow-release 8080:8080 --namespace xops-airflow

## 7. Importing Custom Modules thru kubernetes yaml is possible so far
    Need to define the functions within the yaml file

## 8. Example of Yaml that uses KubernetesPodOperator
 
apiVersion: v1
data:
  chained_task.py: |
    import airflow
    from airflow import DAG
    from airflow.decorators import task
    from functions import start_func, process_func, end_func 
    from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
    from airflow.utils.dates import days_ago
    from kubernetes.client.models import V1VolumeMount, V1Volume

    volume_mount = V1VolumeMount(
        name='custom-modules-volume',
        mount_path='/app/functions',
        read_only=True
    )

    volume = V1Volume(
        name='custom-modules-volume',
        config_map={'name': 'platform'}
    )

    with DAG(
        dag_id = "chained_task",
        start_date = days_ago(3),
        schedule_interval = "@daily",
    ) as dag:
        platform_connector = KubernetesPodOperator(
            namespace='airflow',
            image="chained_task:1.2",
            name="chained_task",
            task_id="chained_task",
            image_pull_policy="Always",
            get_logs=True,
            do_xcom_push=True,
            is_delete_operator_pod=True,
            dag=dag,
            configmaps=['platform'],
            volume_mounts=[volume_mount],
            volumes=[volume]
        )
        
        @task
        def start_task():
            return start_func.start()

        @task
        def process_task(value_from_start_task):
            return process_func.process(value_from_start_task)

        @task
        def end_task(value_from_process_task):
            return end_func.end(value_from_process_task)

        value_from_start_task = start_task()
        value_from_process_task = process_task(value_from_start_task)
        value_from_end_task = end_task(value_from_process_task)

kind: ConfigMap
metadata:
  name: airflowdag13
  namespace: airflow


if Unable to connect to the server: net/http: TLS handshake timeout, unset keme OR minikube stop

#if minikube drv not healthy:
```
sudo chmod 666 /var/run/docker.sock
sudo addgroup --system docker
sudo adduser regi docker
newgrp docker
```

```
put snap in environment var
export PATH=$PATH:/snap/bin
```

### create a volume and volume mount
#create a folder

```mkdir xops-airflow-kube
cd xops-airflow-kube
```

#create a folder for the persistent volume
```
mkdir data
```
#create a persistent volume claim
```
touch pvc.yaml
vim pvc.yaml
```
then paste:
```
apiVersion: v1
kind: PersistentVolume
metadata:
  name: xops-pvc
spec:
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  hostPath:
    path: /home/regi/xops-airflow-kube/data  # Use the full path to your data directory
```

#create a volume
```
touch pv.yaml
vim pv.yaml
```
then paste:
```
apiVersion: v1
kind: PersistentVolume
metadata:
  name: xops-pv
spec:
  capacity:
    storage: 1Gi  # The size of the storage
  accessModes:
    - ReadWriteOnce  # The volume can be mounted as read-write by a single node
  persistentVolumeReclaimPolicy: Retain  # Defines what happens to the PV after it is released
  hostPath:
    path: /home/regi/xops-airflow-kube/data  # The path on the host machine
```

#build the image
```
docker build -t pull-airflow:1.0 .
```