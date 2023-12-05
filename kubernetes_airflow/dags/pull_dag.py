from airflow import DAG
from airflow.operators.dagrun_operator import TriggerDagRunOperator
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from datetime import datetime

default_args = {
    'start_date': datetime(2023, 12, 1),
    # set the schedule interval to daily
    'schedule_interval': '@daily'
}

with DAG('pull_dag', default_args=default_args, schedule_interval='@daily') as dag:

    # Task 1: PullTask
    pull_task_1 = KubernetesPodOperator(
        namespace='airflow-namespace',
        image='pull_task_image:latest',  # Replace with your actual image name and tag
        cmds=["python"],
        arguments=["-c", "from dags.external_functions.pull_operators.pull_task import PullTask; PullTask().pull_task_1()"],
        name="pull-task-1",
        task_id="pull_task_1",
        is_delete_operator_pod=True,
        in_cluster=True,  # Set to False if Airflow is not running inside the same Kubernetes cluster
        get_logs=True,
        dag=dag,
    )

    # Task 2: PullTask
    pull_task_2 = KubernetesPodOperator(
        namespace='airflow-namespace',
        image='pull_task_image:latest',  # Replace with your actual image name and tag
        cmds=["python"],
        arguments=["-c", "from dags.external_functions.pull_operators.pull_task import PullTask; PullTask().pull_task_2()"],
        name="pull-task-2",
        task_id="pull_task_2",
        is_delete_operator_pod=True,
        in_cluster=True,  # Set to False if Airflow is not running inside the same Kubernetes cluster
        get_logs=True,
        dag=dag,
    )

    trigger_push_dag = TriggerDagRunOperator(
        task_id='trigger_push_dag',
        trigger_dag_id="push_dag",
    )

    pull_task_1 >> pull_task_2 >> trigger_push_dag



    # pull_task_1 = PythonOperator(
    #     task_id='pull_task_1',
    #     python_callable=pull_class.pull_task_1,
    #     provide_context=True
    # )
    
    # pull_task_2 = PythonOperator(
    #     task_id='pull_task_2',
    #     python_callable=pull_class.pull_task_2,
    #     provide_context=True
    # )

    # trigger_push_dag = TriggerDagRunOperator(
    #     task_id='trigger_push_dag',
    #     trigger_dag_id="push_dag",
    # )

    # pull_task_1 >> pull_task_2 >> trigger_push_dag