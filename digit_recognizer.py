#coding: utf-8
import csv
from numpy import *
import operator

def load_data(filename, have_labels):
    csvfile = file(filename, 'rb')
    reader = csv.reader(csvfile)
    data = []
    labels = []
    for line in reader:
        data_item = []
        if have_labels:
            labels.append(line[0])
            for i in range(1, 785):
                if line[i] == '0':
                    line[i] = 0
                else:
                    line[i] = 1
            data_item.extend(line[1:])
        else:
            for i in range(0, 784):
                if line[i] == '0':
                    line[i] = 0
                else:
                    line[i] = 1
            data_item.extend(line[:])
        data.append(data_item)
    if have_labels:
        return data, labels
    return data

def classify0(in_x, data_set, labels, k):
    data_set_size = data_set.shape[0]
    mat1 = tile(in_x, (data_set_size, 1))
    diff_mat = mat1 - data_set
    sq_diff_mat = diff_mat ** 2
    sq_distances = sq_diff_mat.sum(axis = 1)
    distances = sq_distances ** 0.5
    sorted_dist_indicies = distances.argsort()
    class_count = {}
    for i in range(k):
        vote_ilabel = labels[sorted_dist_indicies[i]]
        class_count[vote_ilabel] = class_count.get(vote_ilabel, 0) + 1
    sorted_class_count = sorted(class_count.iteritems(), key = operator.itemgetter(1), reverse=True)
    return sorted_class_count[0][0]

train_data, train_labels = load_data('train.csv', True)
test_data = load_data('test.csv', False)
file_written = open('answer.txt', 'w')
number = 1
for item in test_data:
    print "NO." + str(number)
    label = classify0(item, array(train_data), train_labels, 10)
    file_written.write(label)
    print label
    number += 1
    if number == 10:
        break
file_written.close()