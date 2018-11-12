import sys
sys.path.append('/usr/local/Cellar/')
import pcl
import numpy as np

#both list of tuples
def concat_cloud(cloud_a, cloud_b):
	cloud_c = []
	for a in a:
		cloud_c.append(a)

	for b in b:
		cloud_c.append(b)

	cloud = pcl.PointCloud()
	cloud.from_list()
