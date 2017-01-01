import GlobalVars

__author__ = 'admin'

import re
import numpy as np
class Vector():
    NORM_EQ = {'Simple' : "((x + min)/(max - min))", 'Log10' :
        "x = log(10,(x/max))", 'Log2' : "x = log(2,(x/max))", 'Natural log' :
        "x = log(e,(x/max))"}  # key/value pairs of normalisation equations for normalising data

    def __init__(self):             #initialise lists to store data and labels in an encoded, vectorised form,
        self.labels = list()
        self.vectorlist = list()

    def vectorise(self, label):   #convert
        tempVL = list()
        for statement in GlobalVars.Vars.machine_code_instruction_list:
                if None is not statement:
                    emptyVector = np.zeros(shape=(110), dtype=int)
                    for elem in statement:
                        emptyVector = encode(emptyVector, elem,'IS.txt')
                        if elem == (statement[3] or statement[4]):
                            try:
                                emptyVector[len(emptyVector) - 1] = int(str(elem).replace("0x", ""), 16)
                            except Exception as e:
                                print(e)
                    tempVL = [emptyVector]
                    for i in range(20-len(tempVL)):  #add padding to each sequence to prepare for input into network
                        tempVL = np.append(tempVL,np.zeros(shape=(1,110), dtype=int), axis=0)

                GlobalVars.Vars.machine_code_instruction_list_vectorised.append(tempVL)
                GlobalVars.Vars.machine_code_instruction_list_labels.append(label)

    def normalise_dict(self, data, key, *args):
        highestScore =0
        lowestScore = 0
        for d in data:
            if d[key]> highestScore:
               highestScore = d[key]
            if d[key] < lowestScore:
                lowestScore = d[key]
        for d in data:
         x = d[key]
         max = highestScore
         min = lowestScore
         d[key] = eval(Vector.NORM_EQ[args[0]],{'x' : d[key], 'max' : highestScore, 'min' : lowestScore})
        # d[key] = x
        return data


def split(instruction):

    pointer = re.sub('[\s].*?', "", instruction).partition(":")[0]
    instruction = re.sub('[\s].*?', "", instruction).partition(":")[2]
    reg = re.compile('[0-9a-f]{10}([a-z]{3})(.*?$)')
    operator = re.match(reg, instruction).group(1)
    operand_1 = re.match(reg, instruction).group(2).partition(",")[0]
    operand_2 = re.match(reg, instruction).group(2).partition(",")[2]
    return {pointer,instruction,operator,operand_1,operand_2}


def encode(vector, operator, tokenlist):
    try:
        reg = re.compile("^" + str(operator))
        with open(tokenlist, 'r') as inputFile:
            for line_i, line in enumerate(inputFile, 1):
                if re.match(reg, line):
                    vector[line_i] = 1
                    break
    except Exception as e:
        print(e)
    return vector


