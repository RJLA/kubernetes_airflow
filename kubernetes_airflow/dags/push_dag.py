from airflow import DAG
from datetime import datetime
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from kubernetes.client import models as k8s
# from external_functions.push_operators.push_task import PushTask
# from airflow.operators.python_operator import PythonOperator

default_args = {
    'start_date': datetime(2023, 12, 1),
    'schedule_interval': None
}

volume = k8s.V1Volume(
    name='my-volume',
    persistent_volume_claim=k8s.V1PersistentVolumeClaimVolumeSource(claim_name='my-pvc')
)

volume_mount = k8s.V1VolumeMount(
    name='my-volume',
    mount_path='/path/to/mount',
    sub_path=None
)

with DAG('push_dag', default_args=default_args) as dag:
    
    # Task 1: PushTask
    push_task_1 = KubernetesPodOperator(
        namespace='airflow-namespace',
        image='push_task_image:latest',  # Replace with your actual image name and tag
        cmds=["python"],
        arguments=["-c", "from dags.external_functions.push_operators.push_task import PushTask; PushTask().push_task_1()"],
        name="push-task-1",
        task_id="push_task_1",
        is_delete_operator_pod=True,
        in_cluster=True,  # Set to False if Airflow is not running inside the same Kubernetes cluster
        get_logs=True,
        dag=dag,
    )

    # Task 2: PushTask
    push_task_2 = KubernetesPodOperator(
        namespace='airflow-namespace',
        image='push_task_image:latest',  # Replace with your actual image name and tag
        cmds=["python"],
        arguments=["-c", "from dags.external_functions.pull_operators.push_task import PushTask; PushTask().push_task_2()"],
        name="push-task-2",
        task_id="push_task_2",
        is_delete_operator_pod=True,
        in_cluster=True,  # Set to False if Airflow is not running inside the same Kubernetes cluster
        get_logs=True,
        dag=dag,
    )




    # push_class = PushTask()
    # push_task_1 = PythonOperator(
    #     task_id='push_task_1',
    #     python_callable=push_class.push_task_1,
    #     provide_context=True
    # )
    
    # push_task_2 = PythonOperator(
    #     task_id='push_task_2',
    #     python_callable=push_class.push_task_2,
    #     provide_context=True
    # )

    # push_task_1 >> push_task_2