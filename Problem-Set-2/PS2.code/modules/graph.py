from random import shuffle
from ID3 import *
from operator import xor
from parse import parse
import matplotlib.pyplot as plt
import os.path
from pruning import validation_accuracy
import random
import copy

# NOTE: these functions are just for your reference, you will NOT be graded on their output
# so you can feel free to implement them as you choose, or not implement them at all if you want
# to use an entirely different method for graphing
    
def get_graph_accuracy_partial(train_set, attribute_metadata, validate_set, numerical_splits_count, depth, pct):
    '''
    get_graph_accuracy_partial - Given a training set, attribute metadata, validation set, numerical splits count, and percentage,
    this function will return the validation accuracy of a specified (percentage) portion of the trainging setself.
    '''
    data_set1 = []
    temp = []
    if pct !=1:
        for i in range(0, int(pct*len(train_set))):
            rand=random.randint(0,int(pct*len(train_set))-1)
            while(1):
                if temp.count(rand)!=0:
                    rand=random.randint(0,int(pct*len(train_set))-1)
                else:
                    break
            data_set1.append(train_set[rand])
            temp.append(rand)
    else:
        data_set1=train_set

    if data_set1 !=[]:
        pct_tree = ID3(data_set1, attribute_metadata, numerical_splits_count, depth)
        return validation_accuracy(pct_tree, validate_set,attribute_metadata)
    else:
        return 0

def get_graph_data(train_set, attribute_metadata, validate_set, numerical_splits_count, depth, iterations, pcts):
    '''
    Given a training set, attribute metadata, validation set, numerical splits count, iterations, and percentages,
    this function will return an array of the averaged graph accuracy partials based off the number of iterations.
    '''
    graph_data = []
    temp=[]
    for pct in pcts: 
        for j in range(0, iterations):
            origin_splits_count = copy.deepcopy(numerical_splits_count)
            temp.append(get_graph_accuracy_partial(train_set, attribute_metadata, validate_set, origin_splits_count, depth, pct))
        graph_data.append(sum(temp) / len(temp))
        temp = []
    return graph_data

# get_graph will plot the points of the results from get_graph_data and return a graph
def get_graph(train_set, attribute_metadata, validate_set, numerical_splits_count, depth, iterations, lower, upper, increment):
    '''
    get_graph - Given a training set, attribute metadata, validation set, numerical splits count, depth, iterations, lower(range),
    upper(range), and increment, this function will graph the results from get_graph_data in reference to the drange
    percentages of the data.
    '''
    pcts = []
    i = lower
    while i <= upper:
        if i == 0:
            i += increment
            continue
        else:
            pcts.append(i)
        i += increment
    graph_data = get_graph_data(train_set, attribute_metadata, validate_set, numerical_splits_count, depth, iterations, pcts)
    plt.plot(pcts, graph_data, 'r--')
    plt.axis([lower, upper, 0, 100])
    plt.show()