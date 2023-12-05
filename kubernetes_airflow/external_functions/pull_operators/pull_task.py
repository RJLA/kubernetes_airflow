import logging
import json
import os

class PullTask:
    def __init__(self):
        pass
    def pull_task_1(self):
        logging.info("Pull Task 1 executed")

    def pull_task_2(self):
        logging.info(f"Pull Task 2 executed")






# class PullTask:
#     def __init__(self):
#         self.output_path = "/tmp/xcom_return.json"  # Use a path that will be in a shared volume

#     def pull_task_1(self):
#         logging.info("Pull Task 1 executed")
#         str_output = "Pull Task 1 output"
#         # Write output to a file for XCom
#         with open(self.output_path, 'w') as f:
#             json.dump({'task_1_output': str_output}, f)

#     def pull_task_2(self):
#         # Read input from a file for XCom
#         if os.path.exists(self.output_path):
#             with open(self.output_path, 'r') as f:
#                 str_input = json.load(f).get('task_1_output', '')
#             logging.info(f"Pull Task 2 executed: {str_input}")
#         else:
#             logging.error("Pull Task 1 output file not found.")





# import logging

# class PullTask:
#     def __init__(self):
#         pass

#     def pull_task_1(self, **kwargs):
#         logging.info("Pull Task 1 executed")
#         str_output = "Pull Task 1 output"
#         kwargs['ti'].xcom_push(key='task_1_output', value=str_output)

#     def pull_task_2(self, **kwargs):
#         ti = kwargs['ti']
#         str_input = ti.xcom_pull(task_ids='pull_task_1', key='task_1_output')
#         logging.info(f"Pull Task 2 executed: {str_input}")
