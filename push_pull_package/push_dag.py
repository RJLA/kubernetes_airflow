from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from datetime import datetime
from kubernetes.client import models as k8s

default_args = {
    'start_date': datetime(2023, 12, 1),
    'schedule_interval': '@daily'
    }

mount_path = '/home/regi/xops-airflow-kube/mount_data'
# Define volume and claim
volume = k8s.V1Volume(
    name='xops-airflow-volume', # Internal reference name in Airflow
    persistent_volume_claim=k8s.V1PersistentVolumeClaimVolumeSource(claim_name='xops-pvc'), # Name of the PVC in Kubernetes
    )

volume_mount = k8s.V1VolumeMount(
    name='xops-airflow-volume', # Must match the volume reference name above
    mount_path=mount_path, # Path to mount the volume in the container. this will be automatically created if it doesn't exist
    sub_path=None,
    read_only=False,
    )

def create_kubernetes_pod_operator(task_id, arguments):
    return KubernetesPodOperator(
        namespace='xops-airflow',
        image='push-image:1.0',
        cmds=["python", "-c"],
        arguments=[arguments],
        name=task_id.replace('_', '-'),
        task_id=task_id,
        get_logs=True,
        volumes=[volume],
        volume_mounts=[volume_mount],
    )

with DAG('push_dag', default_args=default_args) as dag:
    list_of_tasks = [
        f"from push_functions.push_class_a import PushClassA; PushClassA.main({mount_path})",
        f"from push_functions.push_class_b import PushClassB; PushClassB.main({mount_path})",
        ]

    create_kubernetes_pod_operator('push_task_1', list_of_tasks[0]) >> \
        create_kubernetes_pod_operator('push_task_2', list_of_tasks[1])
