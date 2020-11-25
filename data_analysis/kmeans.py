import k_means_constrained

n = 3
size_min = 10
size_max = 15

clustering = k_means_constrained.KMeansConstrained(n_clusters=n, size_min=size_min, size_max=size_max, random_state=0)

def kmeans_alt(array):
    return clustering.fit(array)
