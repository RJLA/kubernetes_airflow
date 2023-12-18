import logging, os, json, sys

class PullClassA:
    def __init__(self, filepath):
        self.filepath = filepath

    def pull_function_1(self):
        output = {'message': 'pull_function_1() executed'}
        logging.info(output['message'])
        with open(os.path.join(self.filepath, "pull_output1.json"), "w") as file:
            json.dump(output, file)
        return output
    
    def pull_function_2(self):
        with open(os.path.join(self.filepath, "pull_output1.json"), "r") as file:
            pull_function_1_output = json.load(file)
        if pull_function_1_output:
            output = {'message': 'pull_function_2() executed'}
            logging.info(output['message'])
            with open(os.path.join(self.filepath, "pull_output2.json"), "w") as file:
                json.dump(output, file)
            return output

if __name__ == "__main__":
    filepath = sys.argv[1]
    pa = PullClassA(filepath)
    pa.pull_function_1()
    pa.pull_function_2()
