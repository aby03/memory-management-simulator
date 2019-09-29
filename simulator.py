from math import ceil

tlb_algo = "FIFO"
tlb = []
tlb_size = 4
ram_sz = 64
hdd_sz = 256
swap_sz = 128
page_sz = 4
proc_dict = {}

ram = []

class Page:



class Entry:
	# vpn = -1
	# ppn = -1
	# valid = False
	# present = False
	# pid = -1

	def __init__(self, vp, pp):
		self.vpn = vp
		self.ppn = pp
		self.valid = True
		self.present = False

class Process:
	def __init__(self, p, vsz, pti):
		self.pid = p
		self.vsize = vsz
		self.ptable = [Entry(i,-1) for i in range(ceil(vsz/page_sz))]

# Function to Display TLB, RAM, Swap Space
def show_memory():
	print("Memory here")

def insert_tlb(entry):
	if len(tlb) < tlb_size:
		tlb.append(entry)
	else:
		if tlb_algo == "FIFO":
			tlb.pop(0)
			tlb.append(entry)
		elif tlb_algo == "OPT":
			a = 1
			# To do
		elif tlb_algo == "LRU":
			a = 1
			# To Do

def request_mem(pid, address):
	if (proc_dict.has_key(pid)):
		if (proc_dict[pid].pt_index == -1):
			print("Bringing into memory")

		else:

	else:
		print("Invalid process")

# Initialize
if __name__ == "__main__":
	# Read Input
	filename1 = "sample inputfile1.txt"
	with open(filename1) as file_obj:
		proc_lines = file_obj.read().split('\n')

	for i in proc_lines:
		k = i.split()
		proc_dict[k[0]] = Process(k[0],k[1], -1)

	filename2 = "sample inputfile2.txt"
	with open(filename2) as file_obj:
		access_lines = file_obj.read().strip().split('\n')

	print(access_lines)

	for i in range(len(access_lines)):
		k = access_lines[i].split()
		access_lines[i] = (int(k[0]),int(k[1]))

	ram =[]

	for i in access_lines:
		print("Requesting memory for process %d and virtual address %d",i[0],i[1])
		data = request_mem(i[0],i[1])
		print(data)
		print('\n')

	# print(lines)
	# 