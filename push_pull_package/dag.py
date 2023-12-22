"""
This DAG is responsible for pulling data from the source and storing it in the
mounted volume. It then triggers the push DAG to push the data to the destination.
"""
from datetime import datetime
from airflow import DAG
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from kubernetes.client import models as k8s

# Define default args for DAG
DEFAULT_ARGS = {
    'start_date': datetime(2023, 12, 1),
    'schedule_interval': '@daily'
}

# Define mount path
MOUNT_PATH = '/home/regi/xops-airflow-kube/mount_data'

# Define volume
volume = k8s.V1Volume(
    # name here is the internal reference name in Airflow
    name='xops-airflow-volume',
    # claim_name of the PVC in Kubernetes
    persistent_volume_claim=k8s.V1PersistentVolumeClaimVolumeSource(claim_name='xops-pvc'),
)

# Define volume mount
volume_mount = k8s.V1VolumeMount(
    # name must match the volume reference name above
    name='xops-airflow-volume',
    # mount_path is the path to mount the volume in the container.
    # this will be automatically created if it does not exist
    mount_path=MOUNT_PATH,
    sub_path=None,
    read_only=False,
)


def create_kubernetes_pod_operator(task_id, arguments):
    """
    This function creates a KubernetesPodOperator with the given task_id and arguments.
    """
    return KubernetesPodOperator(
        namespace='xops-airflow',
        image='pull-image:1.0',
        cmds=['python', '-c'],
        arguments=[arguments],
        name=task_id.replace('_', '-'),
        task_id=task_id,
        get_logs=True,
        volumes=[volume],
        volume_mounts=[volume_mount],
    )


with DAG('pull_dag', default_args=DEFAULT_ARGS) as dag:
    list_of_tasks = [
        "from pull_functions.pull_class_a import PullClassA; PullClassA.main()", "{mount_path}",
        "from pull_functions.pull_class_b import PullClassB; PullClassB.main()", "{mount_path}",
    ]

    trigger_push_dag = TriggerDagRunOperator(
        task_id='trigger_push_dag',
        trigger_dag_id="push_dag",
    )

    pull_task_1 = create_kubernetes_pod_operator('pull_task_1', list_of_tasks[0])
    pull_task_2 = create_kubernetes_pod_operator('pull_task_2', list_of_tasks[1])
    pull_task_3 = create_kubernetes_pod_operator('pull_task_3', list_of_tasks[2])
    pull_task_4 = create_kubernetes_pod_operator('pull_task_4', list_of_tasks[3])
    pull_task_1 >> pull_task_2 >> pull_task_3 >> pull_task_4 >> trigger_push_dag
