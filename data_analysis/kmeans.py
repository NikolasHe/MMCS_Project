import k_means_constrained
import pandas as pd
# apply heuristic approach of k-means algorithm that allows for controlling the cluster size
n = 3
size_min = 5
size_max = 15

clustering = k_means_constrained.KMeansConstrained(n_clusters=n, size_min=size_min, size_max=size_max, random_state=0)

period_1 = pd.read_csv('demand_stations_period_3', delimiter=',', header=0)
# 31 stations have to be split up between the vans
print(len(period_1))

clustering.fit(period_1[['latitude', 'longitude']])
centers = clustering.cluster_centers_
pred = clustering.fit_predict(period_1[['latitude', 'longitude']])

print(centers)

print(pred)

