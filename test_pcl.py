import sys
import pcl
import math
import argparse
from CloudManager import CloudManager
import sys
import numpy as np
import os
from PIL import Image

c = CloudManager(math.pi/4, math.pi/4, 10, do_round=False)
'''
def test_make_cloud():
	#test concat_points_cloud
	print()
	print(test_make_cloud.__name__)
	c.concat_points_cloud([(1, 2, 3), (4, 5, 6), (6, 7, 8)])
	c.print_cloud()

def test_r_search():
	print()
	print(test_r_search.__name__)
	#test radius search
	result = c.radius_search((1,1,1), 1, 9)
	print("result " + str(result))

def test_replace_with_pts():
	print()
	print(test_replace_with_pts.__name__)
	#test replace space
	items = [1,2,3]
	full = [(x, y, z) for x in items for y in items for z in items]
	c.concat_points_cloud(full)


def test_replace_with_empty():
	print(test_replace_with_empty.__name__)
	#test replace with empty space
	print("before " + str(c.cloud_size()))
	empty = [(1,1,1), (3,3,3)]
	c.concat_points_cloud(empty)
	print("after " + str(c.cloud_size()))
'''
def test_depth_map():
	t = np.zeros((8, 8))
	for j in range(8):
		for i in range(8):
			#t[i][j] = abs(i-j)*int(255/7)
			t[i][j] = 255

	c.concat_depth_map((0, 0, 0), t, 0, 0, 0, 0, 0, 0)
	c.save_cloud("test.txt")

def test_write_cloud():
	c.save_cloud("test.txt")


#test_make_cloud()
#test_replace_with_pts()
#test_r_search()

#test_replace_with_empty()
test_depth_map()
#test_write_cloud()
#p = pcl.PointCloud()














print("test end")