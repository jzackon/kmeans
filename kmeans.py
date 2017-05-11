#Jeremy Zackon
#hw4
#Implementation of the kmeans algorithm with sum squared error for
#seeds and wine quality datasets

import sys
import random
import math

#Cluster class: contains cetroid, list of records, and error.
class Cluster:
    def __init__(self, centr, l, sumsquares):
        self.centroid = centr
        self.records = l
        self.sse = sumsquares

#Preprocessing of seeds data to remove class variable at end of record
def seedsPreprocessing(records):
    for record in records:
        record.pop(len(record) - 1)

    return records

#Preprocessing of wine quality data to remove class variable at end of record
def winequalityPreprocessing(records):
    for record in records:
        record.pop(len(record) - 1)

    return records

#Calculates Euclidean distance between two records of the dataset
def calcDistance(centr, rec):
    total = 0
    for i in range(0, len(centr)):
        diff = centr[i] - rec[i]
        total = total + math.pow(diff, 2)

    return math.sqrt(total)

#Populates the initial clusters with records from the dataset
def populateClusters(clusters, objects):
    x = 0
    for obj in objects:
        if x == len(clusters):
            x = 0
        clusters[x].records.append(obj)
        x = x + 1

#Updates the cluster records by calculating the new minimum distance
#from a record to a centroid
def updateClusters(clusters, objects):

    changeCount = 0

    for obj in objects:
        minDist = math.inf
        for cluster in clusters:
            dist = calcDistance(cluster.centroid, obj)
            if dist < minDist:
                minDist = dist
                clustIndex = clusters.index(cluster)
        if obj not in clusters[clustIndex].records:
            changeCount = changeCount + 1
            for cluster in clusters:
                if obj in cluster.records:
                    cluster.records.remove(obj)
                    break
            clusters[clustIndex].records.append(obj)

    return changeCount

#Updates the centroid of the cluster by averaging the values of the
#records contained in the cluster
def updateCentroids(clusters):

    for cluster in clusters:
        totalsList = []
        for i in range(0, len(cluster.centroid)):
            totalsList.append(0.0)
        for record in cluster.records:
            for i in range(0, len(record)):
                totalsList[i] = totalsList[i] + record[i]
        for i in range(0, len(totalsList)):
            totalsList[i] = totalsList[i]/len(cluster.records)
        cluster.centroid = totalsList

#Calculates the sum squared error for a cluster
def calculateSSE(clusters):

    for cluster in clusters:
        for record in cluster.records:
            total = 0.0
            for i in range(0, len(record)):
                diff = record[i] - cluster.centroid[i]
                total = total + math.pow(diff, 2)
            cluster.sse = cluster.sse + total


def run():

    dataset = sys.argv[1]
    k = int(sys.argv[2])
    outputFile = sys.argv[3]

    records = []

    if(dataset == 'seeds_dataset.txt'):
        f = open(dataset)
        for line in f:
            records.append([float(n) for n in line.split()])
        records = seedsPreprocessing(records)

    if(dataset == 'winequality_whitered.txt'):
        f = open(dataset)
        f.readline()
        for line in f:
            records.append([float(n) for n in line.split(',')])
        records = winequalityPreprocessing(records)

    f.close()
    clusters = []
    check = []

    while(len(check) < k):
        lst = []
        a = random.randint(0, len(records))
        if a not in check:
            check.append(a)
            clust = Cluster(records[a], lst, 0.0)
            clusters.append(clust)


    populateClusters(clusters, records)
    updateClusters(clusters, records)

    done = False
    while(done is False):
        updateCentroids(clusters)
        changeCount = updateClusters(clusters, records)
        if changeCount == 0:
            done = True

    calculateSSE(clusters)
    f = open(outputFile, 'w')
    count = 1
    avgSSE = 0.0
    for cluster in clusters:
        avgSSE = avgSSE + cluster.sse
        f.write('Cluster ' + str(count) + '\n')
        f.write('Centroid: ' + str(cluster.centroid) + '\n')
        f.write('Number of records: ' + str(len(cluster.records)) + '\n')
        f.write('Cluster Sum of Squared Errors: ' + str(cluster.sse) + '\n')
        for record in cluster.records:
            f.write(str(record) + '\n')
        count= count + 1
        f.write('\n')
    avgSSE = avgSSE/len(clusters)
    f.write('Average SSE: ' + str(avgSSE))
    f.close()





run()

