import math
from node import Node
import sys
from data_preprocessing import *

def ID3(data_set, attribute_metadata, numerical_splits_count, depth):
   '''
   See Textbook for algorithm.
   Make sure to handle unknown values, some suggested approaches were
   given in lecture.
   ========================================================================================================
   Input:  A data_set, attribute_metadata, maximum number of splits to consider for numerical attributes,
	maximum depth to search to (depth = 0 indicates that this node should output a label)
   ========================================================================================================
   Output: The node representing the decision tree learned over the given data set
   ========================================================================================================
   '''
   # haven't deal with the unknown values
   preprocessing(data_set, attribute_metadata)
   threshold = 0.1
   if check_homogenous(data_set) != None:
       leaf = Node()
       leaf.label = check_homogenous(data_set)
   else:
        if depth == 0 or entropy(data_set) < threshold:
            leaf = Node()
            leaf.label = mode(data_set)
        else:
            best = pick_best_attribute(data_set, attribute_metadata, numerical_splits_count)
            if best[0] == False:
                leaf = Node()
                leaf.label = mode(data_set)
            else:
                leaf = Node()
                leaf.decision_attribute = best[0]
                leaf.name = attribute_metadata[best[0]]['name']
                depth -= 1
                if str(best[1]) == 'False':
                    leaf.is_nominal = True
                    leaf.children = {}
                    div = split_on_nominal(data_set, best[0])
                    for x in div.keys():
                        leaf.children[x] = ID3(div[x], attribute_metadata, numerical_splits_count, depth)
                else:
                    leaf.is_nominal = False
                    leaf.children = []
                    leaf.splitting_value = best[1]
                    div = split_on_numerical(data_set, best[0], best[1])
                    leaf.children.append(ID3(div[0], attribute_metadata, numerical_splits_count, depth))
                    leaf.children.append(ID3(div[1], attribute_metadata, numerical_splits_count, depth)) 
   return leaf

# def ID3(data_set, attribute_metadata, numerical_splits_count, depth):
#     '''
#     See Textbook for algorithm.
#     Make sure to handle unknown values, some suggested approaches were
#     given in lecture.
#     ========================================================================================================
#     Input:  A data_set, attribute_metadata, maximum number of splits to consider for numerical attributes,
#     maximum depth to search to (depth = 0 indicates that this node should output a label)
#     ========================================================================================================
#     Output: The node representing the decision tree learned over the given data set
#     ========================================================================================================

#     '''
#     preprocessing(data_set, attribute_metadata)
#     if check_homogenous(data_set) != None:
#         root = Node()
#         root.label = check_homogenous(data_set)
#     else: 
#         if depth == 0:
#             root = Node()
#             root.label = mode(data_set)
#         else:
#             best = pick_best_attribute(data_set, attribute_metadata, numerical_splits_count)
#             if best[0] == False:
#                 root = Node()
#                 root.label = mode(data_set)
#             else:
#                 root = Node()
#                 root.decision_attribute = best[0]
#                 root.name = attribute_metadata[best[0]]['name']
#                 depth -= 1
#                 if str(best[1]) == 'False':
#                     root.is_nominal = True
#                     root.children = {}
#                     subsets = split_on_nominal(data_set, best[0])
#                     for splitval in subsets.keys():
#                         root.children[splitval] = ID3(subsets[splitval], attribute_metadata, numerical_splits_count, depth)
#                 else:
#                     root.is_nominal = False
#                     root.children = []
#                     root.splitting_value = best[1]
#                     subsets = split_on_numerical(data_set, best[0], best[1])
#                     root.children.append(ID3(subsets[0], attribute_metadata, numerical_splits_count, depth))
#                     root.children.append(ID3(subsets[1], attribute_metadata, numerical_splits_count, depth)) 
#     return root
#     pass

def check_homogenous(data_set):
    '''
        ========================================================================================================
    Input:  A data_set
    ========================================================================================================
    Job:    Checks if the output value (index 0) is the same for all examples in the the data_set, if so return that output value, otherwise return None.
    ========================================================================================================
    Output: Return either the homogenous attribute or None
    ========================================================================================================
     '''
    #Your code here
    flag = data_set[0][0]
    for i in data_set:
        if i[0] != flag :
            return None
    return flag

# ======== Test Cases =============================
# data_set = [[0],[1],[1],[1],[1],[1]]
# check_homogenous(data_set) ==  None
# data_set = [[0],[1],[None],[0]]
# check_homogenous(data_set) ==  None
# data_set = [[1],[1],[1],[1],[1],[1]]
# check_homogenous(data_set) ==  1

def pick_best_attribute(data_set, attribute_metadata, numerical_splits_count):
    '''
    ========================================================================================================
    Input:  A data_set, attribute_metadata, splits counts for numeric
    ========================================================================================================
    Job:    Find the attribute that maximizes the gain ratio. If attribute is numeric return best split value.
            If nominal, then split value is False.
            If gain ratio of all the attributes is 0, then return False, False
            Only consider numeric splits for which numerical_splits_count is greater than zero
    ========================================================================================================
    Output: best attribute, split value if numeric
    ========================================================================================================
    '''
    # Your code here
    # how to use numerical_splits_count = [20,20]
    max_gainratio = 0
    best_attribute = 0
    best_numeric_split = 0

    for attribute in range(1,len(data_set[0])):
        is_nominal = attribute_metadata[attribute]['is_nominal']
        if is_nominal:
            gain_ratio = gain_ratio_nominal(data_set,attribute)
            if gain_ratio > max_gainratio:
                max_gainratio = gain_ratio
                best_attribute = attribute
        else: 
            if numerical_splits_count[attribute] != 0:
                gain_ratio,numeric_split = gain_ratio_numeric(data_set,attribute,1)
                if gain_ratio >= max_gainratio:
                    max_gainratio = gain_ratio
                    best_attribute = attribute
                    best_numeric_split = numeric_split

    if max_gainratio == 0:
            return (False,False)

    if attribute_metadata[best_attribute]['is_nominal']:
        return (best_attribute,False)
    else:
        numerical_splits_count[best_attribute] -= 1
        return (best_attribute,best_numeric_split)    

# # ======== Test Cases =============================
# numerical_splits_count = [20,20]
# attribute_metadata = [{'name': "winner",'is_nominal': True},{'name': "opprundifferential",'is_nominal': False}]
# data_set = [[1, 0.27], [0, 0.42], [0, 0.86], [0, 0.68], [0, 0.04], [1, 0.01], [1, 0.33], [1, 0.42], [0, 0.51], [1, 0.4]]
# pick_best_attribute(data_set, attribute_metadata, numerical_splits_count) == (1, 0.51)
# attribute_metadata = [{'name': "winner",'is_nominal': True},{'name': "weather",'is_nominal': True}]
# data_set = [[0, 0], [1, 0], [0, 2], [0, 2], [0, 3], [1, 1], [0, 4], [0, 2], [1, 2], [1, 5]]
# pick_best_attribute(data_set, attribute_metadata, numerical_splits_count) == (1, False)

# Uses gain_ratio_nominal or gain_ratio_numeric to calculate gain ratio.

def mode(data_set):
    '''
    ========================================================================================================
    Input:  A data_set
    ========================================================================================================
    Job:    Takes a data_set and finds mode of index 0.
    ========================================================================================================
    Output: mode of index 0.
    ========================================================================================================
    '''
    # Your code here
    list_num = []
    for i in data_set:
        list_num.append(i[0])
    return sorted(list_num)[len(list_num)/2] 
# ======== Test case =============================
# data_set = [[0],[1],[1],[1],[1],[1]]
# mode(data_set) == 1
# data_set = [[0],[1],[0],[0]]
# mode(data_set) == 0

def entropy(data_set):
    '''
    ========================================================================================================
    Input:  A data_set
    ========================================================================================================
    Job:    Calculates the entropy of the attribute at the 0th index, the value we want to predict.
    ========================================================================================================
    Output: Returns entropy. See Textbook for formula
    ========================================================================================================
    '''
    count_1=0
    count_0=0
    freq0=1
    freq1=1
    entro0=1
    entro1=1
    for i in range(len(data_set)):
        if data_set[i][0]==0:
            count_0+=1
        else:
            count_1+=1
    freq0 = (float) (count_0) / (count_0+count_1)
    freq1 = (float) (count_1) / (count_0+count_1) 
    if freq0==1:
        return 0
    if freq1==1:
        return 0  
    entro0 = freq0 * math.log(freq0) / math.log(2)
    entro1 = freq1 * math.log(freq1) / math.log(2)
    return -entro0-entro1
# ======== Test case =============================
# data_set = [[0],[1],[1],[1],[0],[1],[1],[1]]
# entropy(data_set) == 0.811
# data_set = [[0],[0],[1],[1],[0],[1],[1],[0]]
# entropy(data_set) == 1.0
# data_set = [[0],[0],[0],[0],[0],[0],[0],[0]]
# entropy(data_set) == 0


def gain_ratio_nominal(data_set, attribute):
    '''
    ========================================================================================================
    Input:  Subset of data_set, index for a nominal attribute
    ========================================================================================================
    Job:    Finds the gain ratio of a nominal attribute in relation to the variable we are training on.
    ========================================================================================================
    Output: Returns gain_ratio. See https://en.wikipedia.org/wiki/Information_gain_ratio
    ========================================================================================================
    '''
    # Your code here
    numCount = {}
    total =[]
    for i in range(len(data_set)):
        total.append([data_set[i][0]])
        if data_set[i][attribute] in numCount.keys():
            numCount[data_set[i][attribute]].append([data_set[i][0]])
        else:
            temp=[]
            temp.append([data_set[i][0]])
            numCount[data_set[i][attribute]]=temp
    t=len(total)
    sum1=0
    IV=0
    for i in numCount:
        a=len(numCount[i])
        b=(float)(a)/(t)
        sum1 += b * entropy(numCount[i])
        IV -= b*math.log(b,2)
    if IV ==0:
        IV= 0.0000001
    return (entropy(total)-sum1)/IV    

# ======== Test case =============================
# data_set, attr = [[1, 2], [1, 0], [1, 0], [0, 2], [0, 2], [0, 0], [1, 3], [0, 4], [0, 3], [1, 1]], 1
# gain_ratio_nominal(data_set,attr) == 0.11470666361703151
# data_set, attr = [[1, 2], [1, 2], [0, 4], [0, 0], [0, 1], [0, 3], [0, 0], [0, 0], [0, 4], [0, 2]], 1
# gain_ratio_nominal(data_set,attr) == 0.2056423328155741
# data_set, attr = [[0, 3], [0, 3], [0, 3], [0, 4], [0, 4], [0, 4], [0, 0], [0, 2], [1, 4], [0, 4]], 1
# gain_ratio_nominal(data_set,attr) == 0.06409559743967516

def gain_ratio_numeric(data_set, attribute, steps):
    '''
    ========================================================================================================
    Input:  Subset of data set, the index for a numeric attribute, and a step size for normalizing the data.
    ========================================================================================================
    Job:    Calculate the gain_ratio_numeric and find the best single threshold value
            The threshold will be used to split examples into two sets
                 those with attribute value GREATER THAN OR EQUAL TO threshold
                 those with attribute value LESS THAN threshold
            Use the equation here: https://en.wikipedia.org/wiki/Information_gain_ratio
            And restrict your search for possible thresholds to examples with array index mod(step) == 0
    ========================================================================================================
    Output: This function returns the gain ratio and threshold value
    ========================================================================================================
    '''
    # Your code here
    idx=0
    max1=0
    IV=0
    tag=0
    maxtemp=0
    while idx< len(data_set):
        divide= split_on_numerical(data_set,attribute,data_set[idx][attribute])
        templow=divide[0]
        temphigh=divide[1]
        len_low=len(divide[0])
        len_high=len(divide[1])
        ratio_low=(float)(len_low)/(len_low+len_high)
        ratio_high=(float)(len_high)/(len_low+len_high)
        low= []
        for i in range(len(templow)):
            low.append([templow[i][0]])
        high= []
        for i in range(len(temphigh)):
            high.append([temphigh[i][0]])
        total=[]
        total=low+high
        if  len_low==0 or len_high==0:
            maxtemp=0
        else:
            part_low=entropy(low)
            part_high=entropy(high)
            part_total=entropy(total)
            temp_result=part_total-ratio_low*part_low-ratio_high*part_high
            IV = -ratio_low*math.log(ratio_low,2)-ratio_high*math.log(ratio_high,2)
            maxtemp=temp_result/IV   
        if maxtemp>max1:
            max1=maxtemp
            tag=data_set[idx][attribute]
        idx+=steps
    return max1,tag

# ======== Test case =============================
# data_set,attr,step = [[0,0.05], [1,0.17], [1,0.64], [0,0.38], [0,0.19], [1,0.68], [1,0.69], [1,0.17], [1,0.4], [0,0.53]], 1, 2
# gain_ratio_numeric(data_set,attr,step) == (0.31918053332474033, 0.64)
# data_set,attr,step = [[1, 0.35], [1, 0.24], [0, 0.67], [0, 0.36], [1, 0.94], [1, 0.4], [1, 0.15], [0, 0.1], [1, 0.61], [1, 0.17]], 1, 4
# gain_ratio_numeric(data_set,attr,step) == (0.11689800358692547, 0.94)
# data_set,attr,step = [[1, 0.1], [0, 0.29], [1, 0.03], [0, 0.47], [1, 0.25], [1, 0.12], [1, 0.67], [1, 0.73], [1, 0.85], [1, 0.25]], 1, 1
# gain_ratio_numeric(data_set,attr,step) == (0.23645279766002802, 0.29)

def split_on_nominal(data_set, attribute):
    '''
    ========================================================================================================
    Input:  subset of data set, the index for a nominal attribute.
    ========================================================================================================
    Job:    Creates a dictionary of all values of the attribute.
    ========================================================================================================
    Output: Dictionary of all values pointing to a list of all the data with that attribute
    ========================================================================================================
    '''
    # Your code here
    result_dic={}
    temp=[]
    m=0
    for i in range(len(data_set)):
        if data_set[i][attribute] in result_dic.keys():
            result_dic[data_set[i][attribute]].append(data_set[i])
        else:
            temp=[]
            temp.append(data_set[i])
            result_dic[data_set[i][attribute]]=temp
    return result_dic

# ======== Test case =============================
# data_set, attr = [[0, 4], [1, 3], [1, 2], [0, 0], [0, 0], [0, 4], [1, 4], [0, 2], [1, 2], [0, 1]], 1
# split_on_nominal(data_set, attr) == {0: [[0, 0], [0, 0]], 1: [[0, 1]], 2: [[1, 2], [0, 2], [1, 2]], 3: [[1, 3]], 4: [[0, 4], [0, 4], [1, 4]]}
# data_set, attr = [[1, 2], [1, 0], [0, 0], [1, 3], [0, 2], [0, 3], [0, 4], [0, 4], [1, 2], [0, 1]], 1
# split on_nominal(data_set, attr) == {0: [[1, 0], [0, 0]], 1: [[0, 1]], 2: [[1, 2], [0, 2], [1, 2]], 3: [[1, 3], [0, 3]], 4: [[0, 4], [0, 4]]}

def split_on_numerical(data_set, attribute, splitting_value):
    '''
    ========================================================================================================
    Input:  Subset of data set, the index for a numeric attribute, threshold (splitting) value
    ========================================================================================================
    Job:    Splits data_set into a tuple of two lists, the first list contains the examples where the given
	attribute has value less than the splitting value, the second list contains the other examples
    ========================================================================================================
    Output: Tuple of two lists as described above
    ========================================================================================================
    '''
    # Your code here
    result = ()
    high = []
    low = []
    for i in range(len(data_set)):
        if data_set[i][attribute] < splitting_value :
            low.append(data_set[i])
        else:
            high.append(data_set[i])
    result=(low,high)
    return result
# ======== Test case =============================
# d_set,a,sval = [[1, 0.25], [1, 0.89], [0, 0.93], [0, 0.48], [1, 0.19], [1, 0.49], [0, 0.6], [0, 0.6], [1, 0.34], [1, 0.19]],1,0.48
# split_on_numerical(d_set,a,sval) == ([[1, 0.25], [1, 0.19], [1, 0.34], [1, 0.19]],[[1, 0.89], [0, 0.93], [0, 0.48], [1, 0.49], [0, 0.6], [0, 0.6]])
# d_set,a,sval = [[0, 0.91], [0, 0.84], [1, 0.82], [1, 0.07], [0, 0.82],[0, 0.59], [0, 0.87], [0, 0.17], [1, 0.05], [1, 0.76]],1,0.17
# split_on_numerical(d_set,a,sval) == ([[1, 0.07], [1, 0.05]],[[0, 0.91],[0, 0.84], [1, 0.82], [0, 0.82], [0, 0.59], [0, 0.87], [0, 0.17], [1, 0.76]])