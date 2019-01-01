import math
import tools

'''
Assumptions: 
- white - black scale goes from 0 to 255
- width and height pixels are even numbers
- default camera looks in (0,0,1) direction and left side of camera is at (-1,0,0)
- pitch = around y axis, in radians, CCW
- roll = around x axis, in radians, CCW
- yaw = around z axis, in radians, CCW
- depth map image has 0, 0 in the bottom left corner


Considerations:
- make sure rotations about i j vectors are in correct direction, currently assuming right hand rule rotation

'''

class Camera:

	# width and height = number of units of length in width and height the camera can see
	# wr and hr = number of radians of width and height the camera can see
	# wp and hp = number of pixels of width and height in input camera image
	# dark = how far away the camera can "see" using a scale of white to black
	def __init__(self, width, height, wr, hr, wp, hp, dark):
		self.width = width
		self.height = height
		self.wr = wr
		self.hr = hr
		self.wp = wp
		self.hp = hp
		self.darkest = dark

	'''
	Given depth image, convert to points in 3D space
	pos = camera x y z in objective 3D space
	projection = 2D numpy matrix of depth values
	p r y = pitch roll yaw of camera's view
	lp, lr, ly = pitch roll raw of left side of camera, needed to determine rotation of frame about direction of view vector
	'''
	def convert(self, pos, projection, p, r, y, lp, lr, ly):
		i_mid = self.wp/2
		j_mid = self.hp/2

		#direction of camera's view
		vect = tools.pitch([0,0,1], p)
		vect = tools.roll(vect, r)
		vect = tools.yaw(vect, y)

		#parallel to top and bottom of view frame, runs from right to left
		horz = tools.pitch([-1,0,0], lp)
		horz = tools.roll(horz, lr)
		horz = tools.yaw(horz, ly)

		#parallel to left and right of view frame, runs from bottom to top
		vert = tools.ortho(vect, horz)

		new_pts = set()

		for i in range(len(projection)):
			for j in range(len(projection[i])):
				#get radians difference from center
				i_rad = -(i + 0.5 - i_mid)/self.wp * self.wr
				j_rad = -(j + 0.5 - j_mid)/self.hp * self.hr

				#get rotation
				m_i = tools.rmatrix_to_vector(tools.invert(tools.make_unit_vector(vert)), i_rad)
				m_j = tools.rmatrix_to_vector(tools.make_unit_vector(horz), j_rad)

				max_vect = tools.normalize(vect, tools.len_vect(vect))
				max_vect = tools.vector_multiplier(max_vect, tools.darkest)

				#get vector from camera to pixel, with vector in objective 3D space
				pix_dist = projection[i][j] / 255 * self.darkest
				pv = [tools.dot_product(vect, i_rad[0]), tools.dot_product(vect, i_rad[1]), tools.dot_product(vect, i_rad[2])]
				pv = [tools.dot_product(pv, i_rad[0]), tools.dot_product(pv, i_rad[1]), tools.dot_product(pv, i_rad[2])]
				pv = tools.make_unit_vector(pv)
				pix_vect = tools.vector_multiplier(pv, pix_dist)

				#get position of this point in 3D space
				pix_pt = tools.sum_vectors(pos, pix_vect)
				new_pts.append(tools.make_ints(pix_pt))

		return list(new_pts)

if __name__ == "__main__":
	pass






















