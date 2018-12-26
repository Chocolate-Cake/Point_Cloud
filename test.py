import sys
import pcl
import math
import argparse
from CloudManager import CloudManager
import sys
import os
from PIL import Image
from grapher import graph


c = CloudManager()

def test_make_cloud():
	#test concat_points_cloud
	print(test_make_cloud.__name__)
	c.concat_points_cloud([(1, 2, 3), (4, 5, 6), (6, 7, 8)])
	c.print_cloud()

def test_r_search():
	print(test_r_search.__name__)
	#test radius search
	result = c.radius_search((5,6,7), 3)
	print("result " + str(type(result)))
	print("result " + str(result))

def test_replace_with_pts():
	print(test_replace_with_pts.__name__)
	#test replace space
	items = [1,2,3]
	print("before " + str(c.cloud_size()))
	full = [(x, y, z) for x in items for y in items for z in items]
	c.concat_points_cloud(full)
	print("after " + str(c.cloud_size()))

def test_replace_with_empty():
	print(test_replace_with_empty.__name__)
	#test replace with empty space
	print("before " + str(c.cloud_size()))
	empty = [(1,1,1), (3,3,3)]
	c.concat_points_cloud(empty)
	print("after " + str(c.cloud_size()))

def test_write_cloud():
	c.save_cloud("test.txt")


test_make_cloud()
test_r_search()
#test_replace_with_pts()
#test_replace_with_empty()
#test_write_cloud()
#p = pcl.PointCloud()














print("test end")