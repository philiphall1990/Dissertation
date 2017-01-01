import Vector
import NeuralNetwork
import DataandLabelFunctions
import GlobalVars
import BashScripts
import os
import pickle

class Options():

    def __init__(self, path, listOfPackages):
        self.path = path
        self.listOfPackages = listOfPackages
        self.helper = BashScripts.BashScripts()
        self.gv = GlobalVars.Vars()
        self.ff = DataandLabelFunctions.Regex()
        self.vectors = Vector.Vector()

    def find_packages_and_run_objdump(self):
        self.helper.executeObjDump(self.path)
        self.helper.find_and_compile(self.listOfPackages)

    def find_functions(self):

        functionDeclarations = self.ff.get_function_declarations_from_obj_code() #returns a unique list of functions declared in the object files
        self.gv.machine_code_operand_list = self.ff.get_machine_code_operands(self.path) #returns a list of all function references in the object files
        self.ff.calculate_distance(self.gv.machine_code_operand_list,declarationlist=functionDeclarations) # for each function, calculates the number average distance of references to it
        self.gv.source_code_function_list = self.ff.get_source_code_functions('/home/phil/Dropbox/source/') #get all functions from source files

        self.vectors.normalise_dict(functionDeclarations, 'avg distance','Simple')    #normalise the avg distance for all obj code functions
        self.vectors.normalise_dict(self.gv.source_code_function_list, 'avg distance', 'Simple') #normalise the avg source code functions
        self.vectors.normalise_dict(functionDeclarations,'noreferences','Simple') # normalise the no of references to functions in obj code
        self.vectors.normalise_dict(self.gv.source_code_function_list, 'noOfReferences', 'Simple') # normalise the no of references to functions in source code

        #preprocess data for use in neural network
        check = set([(d['name'], os.path.basename(d['filename']).replace('.c','')) for d in self.gv.source_code_function_list])
        functionDeclarations = [d for d in functionDeclarations if (os.path.basename(d['file']).replace('.o.txt',''), d['match'].group(1)) not in check] #removes any functions not also in source code

          # sort by function name and filename#
        functionDeclarations = self.ff.sort_list_of_dicts(functionDeclarations,'file')
        self.gv.source_code_function_list = self.ff.sort_list_of_dicts(self.gv.source_code_function_list, 'name')


        formattedInput = list()
        formattedLabels = list()
        for f in functionDeclarations:
            formattedInput.append([f['avg distance'], f['noreferences'], f['linenumber']])

        for f in formattedLabels:
            formattedLabels.append(f['avg distance'], f['noOfReferences'],f['startnumber'])

        self.picksave(formattedInput, self.path + 'function_declarations')
        self.picksave(formattedLabels, self.path + 'source_code_function_list')



    def find_if_while_statements(self):
        reg = list()
        reg.append(self.gv.regular_expressions['if_statements'])
        reg.append(self.gv.regular_expressions['while_statements'])

        iflist = self.ff.find_statements('', 1, self.gv.regular_expressions['if_statements'],label=[0,1])
        for statement in iflist:
            self.ff.match_line_numbers(statement)
        self.vectors.vectorise([0,1])
        self.gv.source_code_while_statements_list = \
        whilelist = self.ff.find_statements('', 1, self.gv.regular_expressions['while_statements'], label=[1, 0])
        for statement in whilelist:
            self.ff.match_line_numbers(statement)
        self.vectors.vectorise([1,0])


        filenamedata = input('Please choose a name to save the data you have collected\n')
        self.picksave(self.gv.machine_code_instruction_list_vectorised, self.path + filenamedata + '_data.pickle')
        self.picksave(self.gv.machine_code_instruction_list_labels, self.path + filenamedata + '_labels.pickle')




    def run_network(self):
        filelocdata = input('Please input pickle file where data resides:\n')
        fileloclabels = input('Please input pickle file where labels reside\n')
        batch_size = input('Please input batch size: \n')
        epochs = input('Please input no. of epochs to run data\n')
        sequencelength = input('Please input length of sequences for data, including any padding\n')
        dims = input('Please input the number of dimensions in data, i.e. if each unit of data consists of 10 variables, the dimensionality should be 10\n')
        sequencelengthlabels = input('Please input length of sequences for labels, including any padding\n')
        dimslabels = input('Please input the number of dimensions of the labels\n')
        data = self.pickload(fileloc=filelocdata)
        labels = self.pickload(fileloc=fileloclabels)
        x_shape = (len(data)/sequencelength,sequencelength,dims)
        y_shape = (len(labels)/sequencelengthlabels,sequencelengthlabels,dimslabels)
        nn = NeuralNetwork.NeuralNetwork(batch_size=batch_size, epochs=epochs, data=data,labels=labels)

        nn.setupNetwork(x_shape, y_shape, dims, dimslabels, sequencelength)



    def picksave(self, data, fileloc):
        with open(fileloc, 'wb') as handle:
            pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def pickload(self, fileloc):

        with open(fileloc, 'rb') as handle:
            p = pickle.load(handle)

        return p