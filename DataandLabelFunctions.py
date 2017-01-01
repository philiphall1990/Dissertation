import glob
import re
import os
import GlobalVars


'''The Regex Class is used to find data and labels,
with various functions that use regular expressions to find specific variables from the larger datasets.'''
class Regex:
    def __init__(self):
        self.results = list()

    def search(self, fileordirectory, reg, start, findall,file, *args:str):
        output = list()
        pattern = re.compile(reg, re.IGNORECASE)
        if file:
            with open(fileordirectory, 'r') as inputFile:
                if findall:
                    return re.findall(reg,inputFile.read())
                else:
                    for line_i, line in enumerate(inputFile, start):
                        if pattern.search(line):
                            output.append({'match': pattern.search(line), 'line' : line, 'linenumber' : line_i})
                    return output
        else:
            for infile in glob.glob(os.path.join(fileordirectory, '*.o.txt')):
                with open(infile,'r') as inputFile:
                    pattern = re.compile(reg,re.IGNORECASE)
                    if findall:
                        output.append(pattern.findall(inputFile.read()))
                    else:
                        for line_i, line in enumerate(inputFile, start):
                            if pattern.search(line):
                                output.append({'match': pattern.search(line), 'line': line, 'linenumber': line_i, 'file' : infile})
            return output
                #self.results.append({'function no.' : len(self.results), 'match': line.partition(":")[2], 'position': line.partition(":")[0]})

    def get_machine_code_operands(self, inputfile, *token:str):
        output = list()
        matches = (self.search(inputfile,GlobalVars.Vars.regular_expressions['machine code function calls'],1,findall=False,file=False,*token))
        for match in enumerate(matches):
            output.append({'file' : match[1]['file'],'linenumber': match[1]['linenumber'],'function' : match[1]['match'].group(3),'hex' : match[1]['match'].group(2), 'pointer address' : match[1]['match'].group(1)})
        return output

    def get_function_declarations_from_obj_code(self):
        decls = self.search('', GlobalVars.Vars.regular_expressions['machine_code_function_decls'], 1, False, False)
        result = []
        duplicate = False
        for item in decls:
            for r in result:
                if (item['file'] == r['file']) and (item['match'].group(1) == r['match'].group(1)):
                    duplicate = True
            if duplicate == False:
                result.append(item)
            duplicate = False
        return result

    def get_source_code_functions(self, file):
        intermediateOutput = self.find_statements(file,1,'(void | int | char | short | long | float | double)\s*?[a-zA-Z0-9_]*?\(.*?\)', label="[0]")
        output = self.find_references(intermediateOutput)
        return output

    def find_statements(self, path, startline, reg, label):
        output = list()
        startlinenumber = startline
        code = ""
        counter = 0
        isStatement = False
        regEndOfSearch1 = re.compile(";$")
        regEndOfSearch2 = re.compile("}")
        for infile in glob.glob(os.path.join(path, '*.c')):
            print("Working on file {0}".format(infile))
            with open(infile,'r') as inputFile:
                pattern = re.compile(reg, re.IGNORECASE)
                for line_i, line in enumerate(inputFile, 1):
                    if pattern.search( line ) and isStatement == False:
                        startlinenumber = line_i
                        isStatement = True
                    if isStatement:
                        code += line
                        if (regEndOfSearch1.search(line) and code.count("{") == 0) or (regEndOfSearch2.search( line ) and code.count("{") > 0 and code.count("}")== code.count("{")):
                            counter += 1
                            isStatement = False
                            output.append({'count': counter,"filename" : infile, "label" : label, "startnumber" : startlinenumber, "endnumber" : line_i, "code" : code})
                            code = ''
        return output

    def match_line_numbers(self,statement):
        path = statement['filename'].replace(".c",".o.txt")
        for i in range(statement['startnumber'],statement['endnumber'],1):
            reg = re.compile(statement['filename'] + ":" + str(i) + "(.*?)/", re.MULTILINE | re.DOTALL | re.IGNORECASE)
            reg2 = re.compile(GlobalVars.Vars.regular_expressions['machine_code_instruction'])
            try:
                with open(path,'r') as inputFile:
                  for matches in reg.findall(inputFile.read()):
                        newmatch = re.findall(reg2, matches)
                        for match in newmatch:
                                GlobalVars.Vars.machine_code_instruction_list.append(match)
            except Exception as e:
                print(e)

    def find_references(self, functionlist):
        reg = re.compile("(void|int|char|short|long|float|double)\s*?([a-zA-Z0-9_]*?)\(", re.IGNORECASE)
       # functionreferences = {'reffunction', 'linenumber','sameclass'} #function refers to the referenced function, identified by count
        functioncount = 0
        sameclassBool = False
        distance = {'reffunction','cumulativeDistance'}
        for function in functionlist:
            distanceInt = int()
            functioncount = 0
            functionName = re.search(reg,function['code']).group(2) # match any occurrences of the function name (follows type declaration and precedes brackets)
            for infile in glob.glob(os.path.join('', '*.c')):       # look in all source files in given directory
                if infile == function['filename']:                  # test whether current file is the same as declaration file
                    sameclassBool = True
                with open(infile,'r') as inputFile:
                    for line_i, line in enumerate(inputFile.readlines()):           #iterate through each file
                        if re.search(functionName, line):                            #look for function name
                            functioncount += 1
                            #functionreferences.add({'reffunction' : functionlist['count'],'linenumber' : line_i, 'sameclass' : sameclassBool})
                            if sameclassBool:
                                distanceInt += abs(function['startnumber'] - line_i)       #if in same file as declaration the distance between reference and declaration is the difference in line numbers
                            else:
                                distanceInt += abs(function['startnumber'] + line_i)      #if not, the difference is the sum (i.e. cumulative distance from respective class declarations
            if functioncount != 1:
                distanceInt /= functioncount - 1                                                  #get average distance (minus the original declaration, since counter started at 0
            function.update({'reffunction': function['count'], 'name' : functionName,'avg distance': distanceInt, 'noOfReferences' : functioncount})
        return functionlist

    def calculate_distance(self,functionlist,declarationlist):
        sameClassBool = False
        for decl in declarationlist:
            referenceCount = 0
            distance = 0
            for f in functionlist:
                if decl['file'] == f['file']:
                    sameClassBool = True
                if decl['match'].group(1) == f['function']:
                    referenceCount += 1
                    if sameClassBool:
                        distance += abs(f['linenumber'] - decl['linenumber'])  # if in same file as declaration the distance between reference and declaration is the difference in line numbers
                    else:
                        distance += abs(f['linenumber'] - decl['linenumber'])
            if referenceCount != 1:
                distance /=referenceCount- 1
            decl.update({'avg distance' : abs(distance), 'noreferences' : referenceCount})

    def sort_list_of_dicts(self,dictlist, key):
        from operator import itemgetter
        return sorted(dictlist, key=itemgetter(key))






