def preprocessing_for_testdata(data_set, attribute_metadata):
    for entry in data_set:
        for attribute in range(1, len(entry)):
            if entry[attribute] == None:
                entry[attribute] = real_preprocessing(data_set, attribute_metadata, attribute, entry[0])

def preprocessing(data_set, attribute_metadata):
    j = 0
    temp = []
    for i in range(0, len(data_set)):
        if data_set[i][0] == None:
            temp.append(i)
    for i in temp:
        del data_set[i - j] 
        j += 1
    for entry in data_set:
        for attribute in range(1, len(entry)):
            if entry[attribute] == None:
                entry[attribute] = real_preprocessing(data_set, attribute_metadata, attribute, entry[0])
                
def real_preprocessing(data_set, attribute_metadata, attribute, flag):
    temp = {}
    sum = 0
    count = 0
    if attribute_metadata[attribute]['is_nominal'] == False:
        for entry in data_set:
            if entry[attribute] != None and entry[0] == flag:
                sum += entry[attribute]
                count += 1
        return sum / count
    else:
        for entry in data_set:
            if entry[attribute] != None and entry[0] == flag:
                if temp.has_key(entry[attribute]):
                    temp[entry[attribute]] += 1
                else:
                    temp[entry[attribute]] = 1
        for key in temp.keys():
            if temp[key] == max(temp.values()):
                return key