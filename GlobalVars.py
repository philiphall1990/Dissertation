

'''This class holds global variables that persist and are used throughout the program'''
class Vars:
    machine_code_instruction_list = list()
    machine_code_instruction_list_vectorised = list()
    machine_code_instruction_list_labels = list()
    source_code_if_statements_list = list()
    source_code_while_statements_list = list()
    machine_code_operand_list = list()
    source_code_function_list = list()
    regular_expressions = {'machine_code_instruction' :
                               "([0-9A-Za-z]{1,5}):[\sa-zA-Z0-9]{2,}[\t|\s]([a-z]{3,6})\s*?([$%a-z0-9\(\)<>@+-]*?[,|\w])([$%a-z0-9\(\)<>@+-]*?)[#|\n]",
                           'if_statements' :
                               "^\s+?if\s[(].*?[)]",
                           'while_statements' :
                               "^\s+?while\s[(].*?[)]",
                           'machine code function calls' :
                               "([0-9a-f]{1,16}):\s *?([0-9a-zA-Z\s]{2,16}).*?<([a-zA-Z_]*).*?>[\t#|\n]",
                           'machine_code_function_decls' :
                                "([a-zA-Z_]*?)\(\)"}
