import sys
import random
import re
import math

"""
Author: Caleb Smith

Implements kmeans clustering for two-dimensional array of points (integers).

Command line syntax: kmeans.py number_of_clusters input_filename
number_of_clusters must be an integer <= total number of data points
input file must be a text file formatted as two integers per line separated by a space (each integer representing x and y values, respectively, for a single data point).

Example: python kmeans.py 3 input.txt

Outputs to console:
Raw list of data points as read from file. (Once)
List of data points in random order. (Once)
List of data points in each cluster upon first assignment to a cluster. (Once)
List of centroids of each cluster. (After each iteration)
List of data points assigned to each cluster according to distance. (After each iteration)
Final list of data points and their cluster assignments. (Once)

Each iteration will be output to a text file, entitled "output[iteration_number].txt"
Final list of data points and their cluster assignments will be written to text file "final_clusters.txt".

"""
outnum = 1

def random_assignment(point_list, k):

   """

   Assigns data points to clusters.
   
   point_list should be a 2-dimensional list of points ALREADY IN RANDOM ORDER.
   k is an integer representing number of desired clusters.

   Returns a 2-dimensional list of clusters of data points (integers).

   """

   i = 0
   clusters = [[] for i in range(k)]
   for point in point_list:
      clusters[i].append(point)
      i+=1
      if (i==(k)):
         i=0
   return clusters



def calculate_centroid(cluster):

   """
   
   Calculates centroids of a single cluster

   cluster is a 2-dimensional list of data points, each data point being a list of two integers.

   Returns a centroid as a list of integers.

   """

   num_of_points = len(cluster)
   cent_x = sum(point[0] for point in cluster) / num_of_points
   cent_y = sum(point[1] for point in cluster) / num_of_points
   return [cent_x, cent_y]

def assign_closest(point_list, centroids, k):

   """

   Assigns each point from list of data points to the cluster with the closest centroid.

   point_list is a 2-dimensional list of data points, each data point being a list of two integers.

   centroids is a 2-dimensional list of points, each point being a list of two integers.

   k is the desired number of clusters and should match the length of centroids.

   """

   new_clusters = [[] for i in range(k)]
   for point in point_list:
      closest = 0
      i = 0
      shortest_distance = -1
      for centroid in centroids:
         distance = math.sqrt((point[0] - centroid[0])**2 + \
                              (point[1] - centroid[1])**2)
         if distance <= shortest_distance or shortest_distance == -1:
            shortest_distance = distance
            closest = i
         i+=1
      new_clusters[closest].append(point)
   return new_clusters




k = int(sys.argv[1])
input_file_name = sys.argv[2]
input_file = open(input_file_name, "r")
raw_data = input_file.readlines()
input_file.close()
point_list = []
for point in raw_data:
   point_list.append(map(int, point.split()))

while (k > len(point_list)) or (k < 1):
   print "Please enter a value for k that is > 0 and < number of data points"
   k = int(raw_input())

print "\n-----Raw list of points-----\n"
print point_list
   
#Shiffle list of points
random.shuffle(point_list)

print "\n-----Points in random order-----\n"
print point_list

#Assign points to clusters
clusters = random_assignment(point_list, k)
print "\n-----List of points by cluster-----\n"
for cluster in clusters:
   print cluster
   print '\n'

centroids = [[] for i in range(k)]
while True:

   output_file = open("output" + str(outnum) +".txt", "w")

   for i in range(0, k):
      for j in range(0, len(clusters[i])):
         print (str(clusters[i][j][0]) + " " + \
                str(clusters[i][j][1]) + " " + \
                str(i+1) + "\n")
         output_file.write(str(clusters[i][j][0]) + " " + \
                           str(clusters[i][j][1]) + " " + \
                           str(i+1) + "\n")
   output_file.close()

   #Find centroids for clusters

   longest_cluster = 0
   for i in range(0,k):
      if len(clusters[i]) > len(clusters[longest_cluster]):
         longest_cluster = i
   for i in range(0,k):
      if len(clusters[i]) > 0:
         #If cluster is not empty, find centroid
         centroids[i] = calculate_centroid(clusters[i])
      else:
         #If cluster is empty, place centroid at first point in largest cluster
         centroids[i] = clusters[longest_cluster][0]

   print "\n-----Centroids-----\n"
   print centroids

   #Assign points to new clusters based on distance

   print "\n-----Clusters after this iteration-----\n"

   new_clusters = assign_closest(point_list, centroids, k)
   for new_cluster in new_clusters:
      print new_cluster
      print '\n'
   if new_clusters == clusters:
      break #If clusters after this iteration match previous iteration, break loop
   else:
      clusters = new_clusters

   outnum = outnum+1

#Output final clusters
output_file = open("final_clusters.txt", "w")
print "\n-----Final list of points by cluster-----\n"
for i in range(0, k):
   for j in range(0, len(clusters[i])):
      print (str(clusters[i][j][0]) + " " + \
             str(clusters[i][j][1]) + " " + \
             str(i+1) + "\n")
      output_file.write(str(clusters[i][j][0]) + " " + \
                        str(clusters[i][j][1]) + " " + \
                        str(i+1) + "\n")

output_file.close()
