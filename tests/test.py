import inspect
import os.path

def main():
    caller_frame = inspect.stack()[1]
    caller_filename_full = caller_frame.filename
    filename = caller_filename_full
    del caller_frame
    caller_filename_full = os.path.abspath(caller_filename_full)
    cwd = caller_filename_full.replace(filename, '')
    algorithm_name, to_import, algorithm = getDetails(caller_filename_full)
    # print(cwd, algorithm_name, to_import, algorithm)
    createPythonFile(cwd, algorithm_name, to_import, algorithm)
    

def getDetails(caller_filename_full):
    with open(str(caller_filename_full), 'r') as fp:
        lines = fp.readlines()

        index=0
        to_import=[]
        for line in lines:
            if "#import" in line:
                to_import = lines[index+1:len(lines)-1]
                break
            index+=1
        index=0
        for line in to_import:
            if "#end import" in line:
                to_import = to_import[0:index]
                break
            index +=1
        index=0

        algorithm =[]
        for line in lines:
            if "#start" in line:
                algorithm = lines[index+1:len(lines)-1]
                break
            index+=1
        index=0
        for line in algorithm:
            if "#end" in line:
                algorithm = algorithm[0:index]
                break
            index+=1

        if ("".join(algorithm)).count("def") == 1:
            for line in algorithm:
                if "def" in line:
                    line = line.split("def ")
                    line = line[1].split("(")
                    algorithm_name = line[0]
                    break

        elif ("".join(algorithm)).count("def") > 1:
            raise Exception("no more than one function allowed in algorithm block")
        elif (("".join(algorithm)).count("def") < 1):
            raise Exception("no function supplied in algorithm block")

        return algorithm_name, to_import, algorithm

def CreateDockerFile():
    pass

def createPythonFile(cwd, algorithm_name, to_import, algorithm):
    algorithm = algorithm
    # path = str(cwd + 'build')
    # try:
    #     os.mkdir(path)
    # except OSError as error:
    #     if "File exists" in error:
    #         pass
    #     else:
    #         raise error
    with open(str("template.txt"), 'r') as template:
        pythonTemplate = template.readlines()
        template.close()
    index=0
    for line in pythonTemplate:
        if "#insert" in line:
            for i in range(len(algorithm)):
                pythonTemplate.insert(i + 1 + index, str("    " + algorithm[i]))
            break
        index+=1
    
    pythonTemplate = pythonTemplate

    
