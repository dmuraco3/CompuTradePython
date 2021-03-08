import inspect
import os
class CompuTradeEngine():
    def __init__(self):
        self.variables()

        # next block gets the callee's working directory
        frame_info = inspect.stack()[1]
        filepath = frame_info[1]
        filename=filepath
        del frame_info
        filepath = os.path.abspath(filepath)
        filepath = filepath.replace(f'/{filename}', '')
        self.path = filepath

    def variables(self):
        self.algorithmFunc = None
        self.period = '15min'

    def algorithm(self, function):
        lines = inspect.getsource(function)
        temp = lines.split('\n')
        del temp[0]
        index=0
        for line in temp:
            if 'def' in line:
                temp2 = line.split('def ')
                for line in temp2:
                    if line != '':
                        temp2 = line.split('(')
                        self.algorithm_name = temp2[0]
                        break

                subindex=0
                for line in temp2:
                    if '):' in line:
                        temp2 = line.split('):')
                        
                        subsubindex=0
                        temp3 = []
                        for line in temp2:
                            temp2[subsubindex] = temp2[subsubindex].strip()
                            if temp2[subsubindex]!='':
                                temp3.append(temp2[subsubindex])
                            subsubindex+=1
                        temp2=temp3
                                


                        break

                if len(temp2) > 0:
                    temp2.insert(0, 'self,')
                else:
                    temp2.insert(0, 'self')
                    
                temp2.insert(0, 'def ')
                temp2.insert(1, self.algorithm_name)
                temp2.insert(2, '(')
                temp2.insert(len(temp2), '):')
                temp2 = ''.join(temp2)
            

            

            index+=1
        temp[0] = temp2
        index=0
        for line in temp:
            temp[index] = str(line + '\n')
            index+=1

        self.algorithmFunc = temp

        self.BuildPythonFile()

    def config(self, period='15min'):
        self.period = period

    def BuildPythonFile(self):
        if not self.algorithmFunc:
            raise Exception("""\n No algorithm supplied \n put the algorithm decorator over your function like this \n @CompuTradeEngine.algorithm \n def algorithm(): \n \t#algorithm""")
        else:
            __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
            with open(os.path.join(__location__, 'template.txt'), 'r') as fp:
                template = fp.readlines()
                fp.close()
            index=0

            AlgorithmPrep = []
            for line in self.algorithmFunc:
                AlgorithmPrep.append('    ' + line)

            index=0
            for line in template:
                if '#InsertAlgorithm' in line:
                    del template[index]
                    template[index:index] = AlgorithmPrep
                    break
                index+=1
            BuildDirectory = os.path.join(self.path, 'build')
            try:
                os.mkdir(BuildDirectory)
            except FileExistsError:
                pass
            with open(os.path.join(BuildDirectory, str(self.algorithm_name + '.py')), 'w') as file:
                file.writelines(template)