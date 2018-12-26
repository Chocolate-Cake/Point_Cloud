import math

'''
Assumptions: 
- white - black scale goes from 0 to 255
- width and height pixels are even numbers
- default camera looks in (0,0,1) direction and left side of camera is at (-1,0,0)
- pitch = around y axis, in radians, CCW
- roll = around x axis, in radians, CCW
- yaw = around z axis, in radians, CCW
- depth map image has 0, 0 in the bottom left corner


Considerations (not implemented):
- instead of adding i and j vectors to find pixel vector, can rotate view vector about i j axis r radians instead for better accuracy

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

	def round(self, vector, decs):
		result = []
		for num in vector:
			result.append(round(num, decs))
		return result

	#http://planning.cs.uiuc.edu/node102.html
	def yaw(self, vector, angle):
		return self.round([math.cos(angle) * vector[0] - math.sin(angle) * vector[1],
				math.sin(angle) * vector[0] + math.cos(angle) * vector[1],
				vector[2]], 14)

	def pitch(self, vector, angle):
		return self.round([math.cos(angle) * vector[0] + math.sin(angle) * vector[2],
				vector[1],
				-math.sin(angle) * vector[0] + math.cos(angle) * vector[2]], 14)

	def roll(self, vector, angle):
		return self.round([vector[0],
				math.cos(angle) * vector[1] - math.sin(angle) * vector[2],
				math.sin(angle) * vector[1] + math.cos(angle) * vector[2]], 14)

	def ortho(self, u, v):
		return [u[1] * v[2] - v[1] * u[2],
				-(u[0] * v[2] - v[0] * u[2]),
				u[0] * v[1] - v[0] * u[1]]

	def len_vect(self, v):
		return math.sqrt(pow(v[0], 2) + pow(v[1], 2) + pow(v[2], 2))

	def normalize(self, v, n):
		return [v[0]/ n, v[1]/n, v[2]/n]

	def multiple_dist(self, v, dist):
		return [v[0] * dist, v[1] * dist, v[2] * dist]

	def invert(self, v):
		return [-v[0], -v[1], -v[2]]

	def sum_vect(self, v, u):
		return [v[0] + u[0], v[1] + u[1], v[2] + u[2]]

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
		vect = self.pitch([0,0,1], p)
		vect = self.roll(vect, r)
		vect = self.yaw(vect, y)

		#parallel to top and bottom of view frame, runs from right to left
		horz = self.pitch([-1,0,0], lp)
		horz = self.roll(horz, lr)
		horz = self.yaw(horz, ly)

		#parallel to left and right of view frame, runs from bottom to top
		vert = self.ortho(vect, horz)

		new_pts = []

		for i in range(len(projection)):
			for j in range(len(projection[i])):
				i_dist = abs(i + 0.5 - i_mid)/self.wp * self.width
				j_dist = abs(j + 0.5 - j_mid)/self.hp * self.height
				'''
				want distance in units of change in l w, add to view direction vector to find vector of each pixel location
				'''
				#if left of center, use horz vector as is, else flip direction
				if i < i_mid:
					i_vect = self.normalize(horz, self.len_vect(horz))
				else:
					i_vect = self.normalize(self.invert(horz), self.len_vect(horz))

				#if below center, flip direction, else use vert vector as is
				if j < j_mid:
					j_vect = self.normalize(self.invert(vert), self.len_vect(vert))
				else:
					j_vect = self.normalize(vert, self.len_vect(vert))

				max_vect = self.normalize(vect, self.len_vect(vect))
				max_vect = self.multiple_dist(max_vect, self.darkest)

				#get vector from camera to pixel, vector in objective 3D space
				pix_vect = self.sum_vect(self.sum_vect(max_vect, i_vect), j_vect)
				pix_dist = projection[i][j] / 255 * self.darkest
				pix_vect = self.normalize(pix_vect, self.len_vect(pix_vect))
				pix_vect = self.multiple_dist(pix_vect, pix_dist)

				#get position of this point in 3D space
				pix_pt = self.sum_vect(pos, pix_vect)
				new_pts.append(pix_pt)
		return new_pts

if __name__ == "__main__":
	pass






















