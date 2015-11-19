import zmq
import numpy as np

print ("bio::start")
context = zmq.Context()

socket = context.socket(zmq.PAIR)
socket.connect("tcp://localhost:5556")
print ("bio::ready")

class QPainter:
	content = ""

	def to_msg(self):
		return self.content

	def setPen(self,col):
		(r,g,b,a) = col
		if len(self.content) > 0:
			self.content += ";"
		self.content += 
			"p(" + str(r) + 
			"," + str(g) + 
			"," + str(b) + 
			"," + str(a) + ")"
	def drawRect(self, rec):
		(x,y,w,h) = rec
		if len(self.content) > 0:
			self.content += ";"
		self.content += "r(" + str(x) + "," + str(y) + "," + str(w) + "," + str(h) + ")"

def send_painter(p):
	socket.send_string(p.to_msg())

def recv_mat():
	mat_dim = socket.recv_string()
	shape = mat_dim.split(",")
	w = int(shape[0])
	h = int(shape[1])
	mtype = int(shape[2])
	mat_data = socket.recv()
	return _reshape(mat_data, w, h, mtype)


def run_client(track_fun, paint_fun):
   	if not hasattr(track_fun, '__call__'):
	


def _reshape(mat_data, w, h, mtype):
	"""
	M {MATRIX}
	w {width}
        h {height}
	mtype {matrix type}
    	"""
	if mtype in [5, 6, 13, 14, 21, 22, 29, 30]:
		raise Exception("We cannot use floating point matrices so far..")
	
	mod = mtype % 8
	dtype = np.int8 
	if mod == 0:
		dtype = np.uint8
	elif mod == 1:
		dtype = np.int8
	elif mod == 2:
		dtype = np.uint16
	elif mod == 3:
		dtype = np.int16
	elif mod == 4:
		dtype = int
	else:
		raise Exception("Invalid integer type" + str(type))

	div = mtype // 8
	channels = 1
	if div == 0:
		channels = 1
	elif div == 1:
		channels = 2
	elif div == 2:
		channels = 3
	elif div == 3:
		channels = 4
	else:
		raise Exception("Wrong number of channels:" + str(channels))

	buf = memoryview(mat_data)
	M = np.frombuffer(buf, dtype=dtype)
	return np.reshape(M, (w, h, channels))
