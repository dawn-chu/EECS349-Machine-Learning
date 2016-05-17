from node import Node
from ID3 import *
from operator import xor
import copy
from parse import *

# Note, these functions are provided for your reference.  You will not be graded on their behavior,
# so you can implement them as you choose or not implement them at all if you want to use a different
# architecture for pruning.

def reduced_error_pruning(tempnode, temp_originroot, root, originroot, training_set, validation_set, attribute_metadata):
    if tempnode.is_nominal == True:
        subset = split_on_nominal(training_set, tempnode.decision_attribute)
    
        for div in tempnode.children.keys():
            pruning_helper(tempnode,temp_originroot,root,originroot,training_set,validation_set,attribute_metadata,div,subset) 
    else:
        subset = split_on_numerical(training_set, root.decision_attribute, root.splitting_value)
        for i in range(0, 2):
            pruning_helper(tempnode,temp_originroot,root,originroot,training_set,validation_set,attribute_metadata,i,subset)



def pruning_helper(tempnode,temp_originroot,root,originroot,training_set,validation_set,attribute_metadata,div,subset):  
    if tempnode.children[div].label == None:
                newnode = Node()
                newnode.label = mode(subset[div])
                newnode.children = {}
                tempchild = copy.deepcopy(tempnode.children[div])
                tempnode.children[div] = newnode
                prune_acc = validation_accuracy(temp_originroot, validation_set, attribute_metadata)
                acc = validation_accuracy(originroot, validation_set, attribute_metadata)
                if prune_acc >= acc:
                    print prune_acc
                    root.children[div] = newnode
                else:
                    tempnode.children[div] = tempchild
                    reduced_error_pruning(tempnode.children[div], temp_originroot, root.children[div], originroot, subset[div], validation_set, attribute_metadata)


def validation_accuracy(tree, validate_set, attribute_metadata):
    '''
    takes a tree and a validation set and returns the accuracy of the set on the given tree
    '''
    accuracy = 0
    i = 0
    j = 0
    preprocessing(validate_set, attribute_metadata)
    for entry in validate_set:
        if entry[0] != None:
            if entry[0] == tree.classify(entry):
                accuracy += 1
            i += 1
    return float(accuracy) / i * 100
    pass
