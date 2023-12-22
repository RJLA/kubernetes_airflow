import logging, os, json, sys

class PullClassB:
    def __init__(self, filepath):
        self.filepath = filepath

    def pull_function_3(self):
        with open(os.path.join(self.filepath, "pull_output2.json"), "r") as file:
            pull_function_2_output = json.load(file)
        if pull_function_2_output:
            output = {'message': 'pull_function_3() executed'}
            logging.info(output['message'])
            with open(os.path.join(self.filepath, "pull_output3.json"), "w") as file:
                json.dump(output, file)
            return output
    
    def pull_function_4(self):
        with open(os.path.join(self.filepath, "pull_output3.json"), "r") as file:
            pull_function_3_output = json.load(file)
        if pull_function_3_output:
            output = {'message': 'pull_function_4() executed'}
            logging.info(output['message'])
            with open(os.path.join(self.filepath, "pull_output4.json"), "w") as file:
                json.dump(output, file)
            return output

if __name__ == "__main__":
    filepath = sys.argv[1]
    pb = PullClassB(filepath)
    pb.pull_function_3()
    pb.pull_function_4()
