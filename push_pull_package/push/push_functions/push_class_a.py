import logging, os, json, sys

class PushClassA:
    def __init__(self, filepath):
        self.filepath = filepath

    def push_function_1(self):
        output = {'message': 'push_function_1() executed'}
        logging.info(output['message'])
        with open(os.path.join(self.filepath, "push_output1.json"), "w") as file:
            json.dump(output, file)
        return output

    def push_function_2(self):
        with open(os.path.join(self.filepath, "push_output1.json"), "r") as file:
            push_function_1_output = json.load(file)
        if push_function_1_output:
            output = {'message': 'push_function_2() executed'}
            logging.info(output['message'])
            with open(os.path.join(self.filepath, "push_output2.json"), "w") as file:
                json.dump(output, file)
            return output

if __name__ == "__main__":
    filepath = sys.argv[1]
    pa = PushClassA(filepath)
    pa.push_function_1()
    pa.push_function_2()
