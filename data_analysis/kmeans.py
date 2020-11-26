import k_means_constrained
import pandas as pd
# apply heuristic approach of k-means algorithm that allows for controlling the cluster size
n = 3
size_min = 25
size_max = 29

clustering = k_means_constrained.KMeansConstrained(n_clusters=n, size_min=size_min, size_max=size_max, random_state=0)

period_1 = pd.read_csv('C:/Users/Nikolas/PycharmProjects/MMCS_Project/loc_class.csv', delimiter=',', header=0)
# 31 stations have to be split up between the vans
print(len(period_1))

clustering.fit(period_1[['latitude', 'longitude']])
centers = clustering.cluster_centers_
pred = clustering.fit_predict(period_1[['latitude', 'longitude']])

print(centers)

print(pred)

period_1['cluster'] = pred
print(period_1.head())
period_1.to_csv('loc_class.csv')
import matplotlib.pyplot as plt

plt.figure(figsize=(8, 8))
plt.scatter(period_1.latitude, period_1.longitude, c=pred, s=120, cmap='viridis')
plt.scatter(centers[:, 0], centers[:, 1], c='red', s=50, alpha=0.7)

#for i in range(len(close_stations.station_1.unique())):
 #   plt.text(df_close.latitude[i], df_close.longitude[i], str(df_close.station_name[i]), fontsize=8)

plt.xlabel('latitude')
plt.ylabel('longitude')

plt.show()
