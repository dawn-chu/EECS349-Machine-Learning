import os.path
from operator import xor
from parse import *
import csv, collections
import random
from ID3 import *
from node import *
from data_preprocessing import *
# DOCUMENTATION
# ========================================
# this function outputs predictions for a given data set.
# NOTE this function is provided only for reference.
# You will not be graded on the details of this function, so you can change the interface if 
# you choose, or not complete this function at all if you want to use a different method for
# generating predictions.

def create_predictions(tree, predict_source, predict_result_source):
    '''
    Given a tree and a url to a data_set. Create a csv with a prediction for each result
    using the classify method in node class.
    '''
    result_data = parse(predict_source, 'winner')
    result_data_set = result_data[0]
    preprocessing_for_testdata(result_data_set, result_data[1])
    predict_file = csv.reader(open(predict_source, 'rb'))
    predict_result_file = csv.writer(file(predict_result_source, 'wb'))
    i = 0
    for row in predict_file:
        if row[len(row) - 1] == ' winner':
            predict_result_file.writerow(row)
        else:
            row[len(row) - 1] = tree.classify(result_data_set[i])
            predict_result_file.writerow(row)  
            i += 1