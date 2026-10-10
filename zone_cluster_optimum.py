import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.mixture import GaussianMixture

# Load the polygon GeoJSON file
file_path = "Datagov_Pincode_Boundaries.geojson"
gdf = gpd.read_file(file_path)

filtered_gdf = gdf[(gdf['Circle']=='West Bengal ')&(gdf['Division']!='A - N Islands ')]

# Project coordinates to meters for accurate Euclidean distance calculations
# (Uses dynamic local UTM zone projection; defaults back to web mercator if unassigned)
if filtered_gdf.crs is not None:
    # Convert to a metric coordinate system (e.g., EPSG:3857 or local UTM)
    gdf_metric = filtered_gdf.to_crs(epsg=3857) 
else:
    gdf_metric = filtered_gdf


centroids = gdf_metric.geometry.centroid
X = np.array(list(zip(centroids.x, centroids.y)))


bic_scores = []
aic_scores = []

k_range = range(1,100)
for k in k_range:
    gmm = GaussianMixture(n_components=k, random_state=42)
    gmm.fit(X)
   #current_bic = gmm.bic(X)
    bic_scores.append(gmm.bic(X))
    aic_scores.append(gmm.aic(X))

optimal_k_bic = k_range[np.argmin(bic_scores)]
optimal_k_aic = k_range[np.argmin(aic_scores)]

print(f'optimal number of clusters (bic):{optimal_k_bic}')
print(f'optimal number of clusters (aic):{optimal_k_aic}')



fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 5))

# --- Left Subplot: BIC Scores ---
ax1.plot(list(k_range), bic_scores, marker='o', linestyle='-', color='crimson')
ax1.set_title("Bayesian Information Criterion (BIC)", fontsize=12, fontweight="bold")
ax1.set_xlabel("Number of Clusters (K)", fontsize=10)
ax1.set_ylabel("BIC Score", fontsize=10)
ax1.set_xticks(list(k_range)[::5])
ax1.grid(True, linestyle='--', alpha=0.6)

# --- Right Subplot: AIC Scores ---
ax2.plot(list(k_range), aic_scores, marker='s', linestyle='-', color='teal')
ax2.set_title("Akaike Information Criterion (AIC)", fontsize=12, fontweight="bold")
ax2.set_xlabel("Number of Clusters (K)", fontsize=10)
ax2.set_ylabel("AIC Score", fontsize=10)
ax1.set_xticks(list(k_range)[::5])
ax2.grid(True, linestyle='--', alpha=0.6)


plt.suptitle("Information Criteria for Optimal GMM Clusters", fontsize=14, fontweight="bold", y=1.02)

plt.tight_layout()
plt.show()
