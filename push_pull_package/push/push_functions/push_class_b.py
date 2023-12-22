import logging, os, json, sys

class PushClassB:
    def __init__(self, filepath):
        self.filepath = filepath

    def push_function_3(self):
        with open(os.path.join(self.filepath, "push_output2.json"), "r") as file:
            push_function_2_output = json.load(file)
        if push_function_2_output:
            output = {'message': 'push_function_3() executed'}
            logging.info(output['message'])
            with open(os.path.join(self.filepath, "push_output3.json"), "w") as file:
                json.dump(output, file)
            return output
    
    def push_function_4(self):
        with open(os.path.join(self.filepath, "push_output3.json"), "r") as file:
            push_function_3_output = json.load(file)
        if push_function_3_output:
            output = {'message': 'push_function_4() executed'}
            logging.info(output['message'])
            with open(os.path.join(self.filepath, "push_output4.json"), "w") as file:
                json.dump(output, file)
            return output

if __name__ == "__main__":
    filepath = sys.argv[1]
    pb = PushClassB(filepath)
    pb.push_function_3()
    pb.push_function_4()
