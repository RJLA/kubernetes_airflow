import logging
import json
import os

class PushTask:
    def __init__(self):
        pass

    def push_task_1(self):
        logging.info("Push Task 1 executed")

    def push_task_2(self):
        logging.info(f"Push Task 2 executed")


# class PushTask:
#     def __init__(self):
#         self.output_path = "/tmp/xcom_return.json"  # Use a path that will be in a shared volume

#     def push_task_1(self):
#         logging.info("Push Task 1 executed")
#         str_output = "Push Task 1 output"
#         # Write output to a file for XCom
#         with open(self.output_path, 'w') as f:
#             json.dump({'task_1_output': str_output}, f)

#     def push_task_2(self):
#         # Read input from a file for XCom
#         if os.path.exists(self.output_path):
#             with open(self.output_path, 'r') as f:
#                 str_input = json.load(f).get('task_1_output', '')
#             logging.info(f"Push Task 2 executed: {str_input}")
#         else:
#             logging.error("Push Task 1 output file not found.")



# import logging

# class PushTask:
#     def __init__(self):
#         pass

#     def push_task_1(self, **kwargs):
#         logging.info("Push Task 1 executed")
#         str_output = "Push Task 1 output"
#         kwargs['ti'].xcom_push(key='task_1_output', value=str_output)

#     def push_task_2(self, **kwargs):
#         ti = kwargs['ti']
#         str_input = ti.xcom_pull(task_ids='push_task_1', key='task_1_output')
#         logging.info(f"Push Task 2 executed: {str_input}")
        