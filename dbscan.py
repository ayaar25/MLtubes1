from math import sqrt

def euclidean_distance(instance1, instance2):
    return sqrt((instance1[0]-instance2[0])**2 + (instance1[1]-instance2[1])**2 + (instance1[2]-instance2[2])**2
        + (instance1[3]-instance2[3])**2)

def make_distance_matrix(array):
    distance_matrix = []
    for i in range(0, len(array)):
        distance_matrix.append([])
        for j in range (0, len(array)):
            distance_matrix[i].append(euclidean_distance(array[i], array[j]))
    return distance_matrix

def make_clusters(distance_matrix, epsilon):
    clusters = []
    for i in range(0, len(distance_matrix)):
        clusters.append([])
        for j in range (0, len(distance_matrix[i])):
            if (distance_matrix[i][j] <= epsilon):
                clusters[i].append(j)
    return clusters

def merge_clusters(clusters, min_pts):
    merged_clusters = []
    for i in range(0, len(clusters)):
        if (len(clusters[i]) >= min_pts):
            if (len(merged_clusters) == 0):
                merged_clusters.append(clusters[i])
            else:
                already_listed = False
                for j in range(0, len(merged_clusters)):
                    if (not set(merged_clusters[j]).isdisjoint(set(clusters[i]))):
                        merged_clusters[j] = list(set(merged_clusters[j]).union(set(clusters[i])))
                        already_listed = True
                        break;
                    else:
                        pass
                if (not already_listed):
                    merged_clusters.append(clusters[i])
        else:
            pass
    return merged_clusters

def DBSCAN_predict(data, epsilon, min_pts):
    distance_matrix = make_distance_matrix(data)
    clusters = make_clusters(distance_matrix, epsilon)
    merged_clusters = merge_clusters(clusters, min_pts)
    labels = []
    for i in range(0, len(data)):
        labels.append(-1)
    for i in range(0, len(merged_clusters)):
        for j in range(0, len(merged_clusters[i])):
            labels[merged_clusters[i][j]] = i
    return labels

def calculateAccuracy(predictions, actual_targets):
    right_counts = 0
    for i in range(0,len(predictions)):
        if (predictions[i] == actual_targets[i]):
            right_counts += 1
    return (right_counts/len(predictions))

from sklearn import datasets
iris = datasets.load_iris()

print(calculateAccuracy(DBSCAN_predict(iris.data, 1, 2), iris.target))