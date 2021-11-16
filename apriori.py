#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 3, 03:09:11 2021
@author: ayushi
Data Mining Mini project
APRIORI ALGORITHM
"""

import sys
import time
from itertools import chain, combinations
from collections import defaultdict
import pandas as pd

#Returning non empty subsets
def fun_subset(arr):
    return chain(*[combinations(arr, i + 1) for i, a in enumerate(arr)])

#Calculate support and return freq itemsets that satisfy min support
def fun_minsup(itemSet, transactionList, minSupport, freqSet):
#calculate support for itemset and return the subsets that satisfy min support condition
    _itemSet = set()
    localSet = defaultdict(int)

    for item in itemSet:
        for transaction in transactionList:
            if item.issubset(transaction):
                freqSet[item] += 1
                localSet[item] += 1

    for item, count in localSet.items():
        support = float(count) / len(transactionList)

        if support >= minSupport:
            _itemSet.add(item)

    return _itemSet

#Join a set with itself and returns the n-element itemsets
def fun_join(itemSet, length):
    return set(
        [i.union(j) for i in itemSet for j in itemSet if len(i.union(j)) == length]
    )


def fun_gettransaction(data):
    transactionList = list()
    itemSet = set()
    for record in data:
        transaction = frozenset(record)
        transactionList.append(transaction)
        for item in transaction:
            itemSet.add(frozenset([item]))  # Generate 1-itemSets
    return itemSet, transactionList

#run aprori algorithm
def fun_runapriori(data_iter, minSupport, minConfidence):
    itemSet, transactionList = fun_gettransaction(data_iter)

    freqSet = defaultdict(int)
    largeSet = dict()
    # Global dictionary which stores (key=n-itemSets,value=support)
    # which satisfy minSupport

    assocRules = dict()
    # Dictionary which stores Association Rules

    oneCSet = fun_minsup(itemSet, transactionList, minSupport, freqSet)

    currentLSet = oneCSet
    k = 2
    while currentLSet != set([]):
        largeSet[k - 1] = currentLSet
        currentLSet = fun_join(currentLSet, k)
        currentCSet = fun_minsup(
            currentLSet, transactionList, minSupport, freqSet
        )
        currentLSet = currentCSet
        k = k + 1

    def fun_support(item):
#local function to return freq itemset
        return float(freqSet[item]) / len(transactionList)

    toRetItems = []
    for key, value in largeSet.items():
        toRetItems.extend([(tuple(item), fun_support(item)) for item in value])

    toRetRules = []
    for key, value in list(largeSet.items())[1:]:
        for item in value:
            _fun_subset = map(frozenset, [x for x in fun_subset(item)])
            for element in _fun_subset:
                remain = item.difference(element)
                if len(remain) > 0:
                    confidence = fun_support(item) / fun_support(element)
                    if confidence >= minConfidence:
                        toRetRules.append(((tuple(element), tuple(remain)), confidence))
    return toRetItems, toRetRules

#prints the generated itemset
def fun_results(items, rules):
    for item, support in sorted(items, key=lambda x: x[1]):
        print("item: %s , %.3f" % (str(item), support))
    print("\n------------------------ RULES:")
    for rule, confidence in sorted(rules, key=lambda x: x[1]):
        pre, post = rule
        print("Rule: %s ==> %s , %.3f" % (str(pre), str(post), confidence))

#print the final frequent itemsets with min support and confience 
def to_str_results(itemset, rules):
    i, r = [], []
    for item, supp in sorted(itemset, key=lambda x: x[1]):
        x = "item: %s , %.3f" % (str(item), supp)
        i.append(x)

    for rule, conf in sorted(rules, key=lambda x: x[1]):
        pre, post = rule
        x = "Rule: %s ==> %s , %.3f" % (str(pre), str(post), conf)
        r.append(x)

    return i, r

# Functiion to read data from file and return a generator
def dataFromFile(fname):
    with open(fname, "rU") as file_iter:
        for i in file_iter:
# Remove trailing comma
            i = i.strip().rstrip(",")  
            data = frozenset(i.split(","))
            yield data


if __name__ == "__main__":
    
     time1 = time.time()
#Passing file
     inFile = dataFromFile('new.csv')
#setting minimum support and confidence interval
     minSup = 0.15
     minConf = 0.6
     
#run the algorithm
     items, rules = fun_runapriori(inFile, minSup, minConf)
#Printing the results
     fun_results(items, rules)
     time2 = time.time()
     testtime = time2 - time1
     print ("\n")
     print ("The runtime for this algorithm(with a sampling factor of .6 and a min_supp = .6) is" + " " + str(testtime) + " seconds.")