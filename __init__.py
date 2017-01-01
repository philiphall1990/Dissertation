import pickle

import GlobalVars
import DataandLabelFunctions

__author__ = 'admin'
__name__ = '__main__'

import Vector
import BashScripts

import NeuralNetwork
import re
import os
import io
import DataandLabelFunctions
import GlobalVars as gv
import Options
def main():

    optionClass = Options.Options(path,listOfPackages)
    if option == str(1):
        optionClass.find_packages_and_run_objdump()
    if option == str(2):
        optionClass.find_functions()
    if option == str(3):
        optionClass.find_if_while_statements()
    if option == str(4):
        optionClass.run_network()
    else:
        print('I\'m sorry, I did not understand your input, please restart the program and try again.')
        exit()




if __name__ == "__main__":

    listOfPackages = ['abook', 'alot', 'alpine', 'altermime', 'amavisd-milter', 'amavisd-new', 'archivemail'] #sample of a chosen array of package names as exmaple of input

    path = input('Please choose your home directory, where any source and object files may reside\n')
    option = input("Please type the number for the action you wish to take: \n 1) find packages and execute object dump, \n 2) find functions in data \n 3) find if and while statements \n 4) run network\n")

    main()