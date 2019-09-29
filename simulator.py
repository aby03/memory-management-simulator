from math import ceil

tlb_algo = "FIFO"
tlb = []
tlb_size = 4
ram_sz = 60
hdd_sz = 256
swap_sz = 8
page_sz = 4
proc_dict = {}
kernel_pt = {}

ram = []
swap = []
ram_pages_free = 0;
swap_pages_free = 0;
ram_numpages = 0;
swap_numpages = 0;

# class Page:

class TLB_Entry:
	def __init__(self):
		self.pid = -1
		self.vpn = -1;
		self.ppn = -1;
		self.valid = False;

	def insert(self,pid,vpn,ppn):
		self.pid = pid
		self.vpn = vpn;
		self.ppn = ppn;
		self.valid = True;

	def checkEqual(pid, vpn):
		if (self.pid == pid and self.vpn == vpn):
			return True
		return False;

class PT_Entry:
	# vpn = -1
	# ppn = -1
	# valid = False
	# present = False
	# pid = -1

	def __init__(self, pp, pres):
		self.ppn = pp
		self.present = pres

class Process:
	def __init__(self, p, vsz):
		self.pid = p
		self.vsize = vsz
		self.ptable = [None for i in range(ceil(vsz/page_sz))]

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

def check_tlb(pid, page_num):
	for i in tlb:
		if (i.valid == True and i.checkEqual(pid, page_num) == True):
			print("TLB hit")
			return True
	print("TLB Miss")
	return False


def access_mem(pid, address):
	page_num = address/page_sz
	if (proc_dict.has_key(pid)):
		if(not check_tlb(pid,page_num)):
			if (not check_ram(pid, page_num)):
				check_kpt(pid,page_num)
	else:
		print("Invalid Process ",pid)

def insert_proc(pid, v_size):
	num_pages = ceil(v_size/page_sz)
	global ram_pages_free, swap_pages_free

	if (num_pages > ram_pages_free + swap_pages_free):
		print("Dropping process " + str(pid) + ". Not enough memory.")
		return

	curr_proc = Process(pid, v_size)

	page_count = 0;
	for i in range(len(ram)):
		if (page_count == num_pages):
			proc_dict[pid] = curr_proc
			return
		if (ram[i] == None):
			ram[i] = (pid,page_count)
			curr_proc.ptable[page_count] = PT_Entry(i,True)
			page_count += 1
			ram_pages_free -= 1

	for i in range(len(swap)):
		if (page_count == num_pages):
			proc_dict[pid] = curr_proc
			return
		if (swap[i] == None):
			swap[i] = (pid,page_count)
			curr_proc.ptable[page_count] = PT_Entry(i,False)
			kernel_pt[(pid,page_count)] = i
			page_count += 1
			swap_pages_free -= 1
	proc_dict[pid] = curr_proc
	return

# Initialize
if __name__ == "__main__":
	ram_numpages = ceil(ram_sz/page_sz)
	swap_numpages = ceil(swap_sz/page_sz)
	ram = [None for i in range(ram_numpages)]
	swap = [None for i in range(swap_numpages)]
	tlb = [TLB_Entry() for i in range(tlb_size)]
	ram_pages_free = ram_numpages
	swap_pages_free = swap_numpages

	
	# Read Input
	filename1 = "sample inputfile1.txt"
	with open(filename1) as file_obj:
		proc_lines = file_obj.read().split('\n')

	for i in proc_lines:
		k = i.split()
		insert_proc(int(k[0]),int(k[1]))

	print(ram)
	print(kernel_pt)


	# filename2 = "sample inputfile2.txt"
	# with open(filename2) as file_obj:
	# 	access_lines = file_obj.read().strip().split('\n')

	# print(access_lines)

	# for i in range(len(access_lines)):
	# 	k = access_lines[i].split()
	# 	access_lines[i] = (int(k[0]),int(k[1]))

	

	# for i in access_lines:
	# 	print("Requesting memory for process %d and virtual address %d",i[0],i[1])
	# 	data = access_mem(i[0],i[1])
	# 	print(data)
	# 	print('\n')

	# print(lines)
	# 