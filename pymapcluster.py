##
import globalmaptiles as globaltiles
from math import cos, sin, atan2, sqrt
##
 
def center_geolocation(geolocations):
    """
    Provide a relatively accurate center lat, lon returned as a list pair, given
    a list of list pairs.
    ex: in: geolocations = ((lat1,lon1), (lat2,lon2),)
        out: (center_lat, center_lon)
    """
    x = 0
    y = 0
    z = 0
 
    for lat, lon in geolocations:
        lat = float(lat)
        lon = float(lon)
        x += cos(lat) * cos(lon)
        y += cos(lat) * sin(lon)
        z += sin(lat)
 
    x = float(x / len(geolocations))
    y = float(y / len(geolocations))
    z = float(z / len(geolocations))
 
    return (atan2(y, x), atan2(z, sqrt(x * x + y * y)))

def latlng_to_zoompixels(mercator, lat, lng, zoom):
    mx, my = mercator.LatLonToMeters(lat, lng)
    pix = mercator.MetersToPixels(mx, my, zoom)
    return pix

def in_cluster(center, radius, point):
    return (point[0] >= center[0] - radius) and (point[0] <= center[0] + radius) \
       and (point[1] >= center[1] - radius) and (point[1] <= center[1] + radius)

def cluster_markers(mercator, latlngs, zoom, gridsize=50):
    """
    Args:
        mercator: instance of GlobalMercator()
        latlngs: list of (lat,lng) tuple
        zoom: current zoom level
        gridsize: cluster radius (in pixels in current zoom level)
    Returns:
        centers: list of indices in latlngs of points used as centers
        clusters: list of same length as latlngs giving assigning each point to
                  a cluster
    """
    centers = []
    clusters = []
    for i, (lat, lng) in enumerate(latlngs):
        point_pix = latlng_to_zoompixels(mercator, lat, lng, zoom)
        assigned = False
        for cidx, c in enumerate(centers):
            center = latlngs[c]
            center = latlng_to_zoompixels(mercator, center[0], center[1], zoom)
            if in_cluster(center, gridsize, point_pix):
                # Assign point to cluster
                clusters.append(cidx)
                assigned = True
                break
        if not assigned:
            # Create new cluster fo point
            #TODO center_geolocation the center!
            centers.append(i)
            clusters.append(len(centers) - 1)
    return centers, clusters

def create_clusters_centers(markers, zoom, radius):
    mercator = GlobalMercator()
    centers, clusters = clust.cluster_markers(mercator, markers, zoom, radius);
    centers_markers = [markers[i] for i in centers]
    return centers_markers, clusters

def cluster_json(clust_marker, clust_size):
    return {
        'longitude': clust_marker.lon,
        'latutude': clust_marker.lat,
        'size': clust_size
    }

def get_cluster_size(index, clusters):
    from collections import Counter
    #TODO: don't call Counter for every cluster in the array
    return Counter[index](clusters)

def get_clusters_json(markers, zoom, radius):
    centers, clusters = create_clusters_centers(marker, zoom, radius)
    json_clusts=[]

    for i, point in enumerate(centers):
        json_clusts.append(cluster_json(point), get_clusters_json(i, clusters))

    return {
        'clusters': json_clusts
    }

##
if __name__ == '__main__':
    ##
    mercator = globaltiles.GlobalMercator()
    latlngs = [(28.43, 8), (28.43, 8), (28.44, 8), (35, 8)]
    centers, clusters = cluster_markers(mercator, latlngs, 21)
    ##
