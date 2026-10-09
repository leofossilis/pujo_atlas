import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture
from matplotlib.colors import ListedColormap

colors_tab20 = plt.colormaps['tab20'].colors
colors_tab10 = plt.colormaps['tab10'].colors
combined_colors = colors_tab20 + colors_tab10
tab30_cmap = ListedColormap(combined_colors, name='tab30')

# Load the polygon GeoJSON file
file_path = "Datagov_Pincode_Boundaries.geojson"
gdf = gpd.read_file(file_path)

ex_div =  ['A_N Islands ','Sikkim ']

filtered_gdf = gdf[(gdf['Circle']=='West Bengal ')&(gdf['Division']!='A - N Islands ')]

# Project coordinates to meters for accurate Euclidean distance calculations
# (Uses dynamic local UTM zone projection; defaults back to web mercator if unassigned)
if filtered_gdf.crs is not None:
    # Convert to a metric coordinate system (e.g., EPSG:3857 or local UTM)
    gdf_metric = filtered_gdf.to_crs(epsg=3857) 
else:
    gdf_metric = filtered_gdf

#  Extract the centroid point coordinates in meters
centroids = gdf_metric.geometry.centroid
X = list(zip(centroids.x, centroids.y))

# gausian mixture model for clustering
gmm = GaussianMixture(n_components=21, random_state=42)
filtered_gdf["cluster_id"] = gmm.fit_predict(X)

print(filtered_gdf['cluster_id'].unique())



fig, ax = plt.subplots(figsize=(10, 8))
#cmap_discrete = plt.colormaps['gist_rainbow'].resampled(25)

filtered_gdf.plot(
    column="cluster_id",
    cmap= tab30_cmap,
    categorical=True,
    legend=False,
    edgecolor="black",         # Thin border color for the polygons
    linewidth=0.15,             # Thickness of polygon borders
    alpha=0.75,                # Transparency setting (0 = clear, 1 = solid)
    ax=ax,
    legend_kwds={'title': "Cluster ID", 'loc': "upper right"}
)

# Clean up the map layout
ax.set_title("Geographic Polygon Clusters", fontsize=14, fontweight="bold", pad=15)
ax.set_axis_off()  

# Display the map
plt.tight_layout()
plt.show()
