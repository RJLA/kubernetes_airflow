"""
This DAG is responsible for pulling data from the source and storing it in the
mounted volume. It then triggers the push DAG to push the data to the destination.
"""
from datetime import datetime
from airflow import DAG
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from kubernetes.client import models as k8s

DEFAULT_ARGS = {
    'start_date': datetime(2023, 12, 1),
    'schedule_interval': '@daily'
}

# This is the path to the mounted volume in the container
MOUNT_PATH = '/home/regi/xops-airflow-kube/mount_data'

# Define volume
volume = k8s.V1Volume(
    # name is the internal reference name in Airflow
    name='xops-airflow-volume',
    # claim_name of the PVC in Kubernetes
    persistent_volume_claim=k8s.V1PersistentVolumeClaimVolumeSource(claim_name='xops-pvc'),
)

# Define volume mount
volume_mount = k8s.V1VolumeMount(
    name='xops-airflow-volume',  # name match the volume reference name above
    mount_path=MOUNT_PATH,  # mount_path is the path to mount the volume in the container.
)


def create_kubernetes_pod_operator(task_id, arguments):
    """
    Creates a KubernetesPodOperator with specified parameters.

    Args:
        task_id (str): The ID for the Airflow task.
        This is used to uniquely identify the task within the DAG.
        arguments (str): The arguments to pass to the command running in the Kubernetes pod.

    Returns:
        KubernetesPodOperator: Configured pod operator for use in an Airflow DAG.

    Note: The function assumes that 'volume' and 'volume_mount' are predefined.
    """
    return KubernetesPodOperator(
        namespace='xops-airflow',  # Namespace in Kubernetes where the pod will be deployed
        image='pull-image:1.0',  # Docker image to use for the pod
        cmds=["python", "-c"],  # Command to run in the container
        arguments=[arguments],  # Arguments passed to the command
        name=task_id.replace('_', '-'),  # Name of the pod (derived from task_id)
        task_id=task_id,  # Unique task ID for Airflow
        get_logs=True,  # If True, Airflow will fetch logs from the pod
        volumes=[volume],  # List of volumes to attach to the pod
        volume_mounts=[volume_mount],  # List of volume mounts in the pod
    )


with DAG('pull_dag', default_args=DEFAULT_ARGS) as dag:
    list_of_tasks = [
        f"from pull_functions.pull_class_a import PullClassA; PullClassA.main('{MOUNT_PATH}')",
        f"from pull_functions.pull_class_b import PullClassB; PullClassB.main('{MOUNT_PATH}')",
    ]

    trigger_push_dag = TriggerDagRunOperator(
        task_id='trigger_push_dag',
        trigger_dag_id="push_dag",
    )

    pull_task_1 = create_kubernetes_pod_operator('pull_task_1', list_of_tasks[0])
    pull_task_2 = create_kubernetes_pod_operator('pull_task_2', list_of_tasks[1])

    pull_task_1 >> pull_task_2 >> trigger_push_dag
