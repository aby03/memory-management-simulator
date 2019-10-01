from math import ceil

tlb_algo = "OPT"
pr_algo = "OPT"
tlb = []
tlb_lru = []
tlb_size = 4
ram_sz = 60
hdd_sz = 256
swap_sz = 128
page_sz = 4
proc_dict = {}
kernel_pt = {}

ram = []
swap = []
ram_pages_free = 0;
swap_pages_free = 0;
ram_numpages = 0;
swap_numpages = 0;
access_count = 0

fifo_pr = []

class TLB_Entry:
	def __init__(self):
		self.pid = -1
		self.vpn = -1;
		self.ppn = -1;
		self.valid = False;

	def insert(self, pid, vpn, ppn):
		self.pid = pid
		self.vpn = vpn;
		self.ppn = ppn;
		self.valid = True;

	def checkEqual(self, pid, vpn):
		if (self.pid == pid and self.vpn == vpn):
			return True
		return False;

	def __string__(self):
		return "(" + str(self.pid) + "," + str(self.vpn) + "," + str(self.ppn) + ")" 

	def printfn(self):
		print("(" + str(self.pid) + "," + str(self.vpn) + "," + str(self.ppn) + "," + str(self.valid) + ")")

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
		self.ptable = [None for i in range(int(ceil(vsz/page_sz)))]

# Function to Display TLB, RAM, Swap Space
def show_memory():
	print("Memory here")

def insert_tlb(entry):
	if tlb_algo == "FIFO":
		# Add if empty space
		for i in range(len(tlb)):
			if (not tlb[i].valid):
				tlb[i] = entry
				return
		# Replace with FIFO
		tlb.pop(0)
		tlb.append(entry)
	elif tlb_algo == "LRU":
		# Add if empty space
		for i in range(len(tlb)):
			if (not tlb[i].valid):
				tlb[i] = entry
				tlb_lru[i] = access_count
				return
		# Replace with LRU
		index = tlb_lru.index(min(tlb_lru))
		tlb[index] = entry
		tlb_lru[index] = access_count
	elif tlb_algo == "OPT":
		# Add if empty space
		for i in range(len(tlb)):
			if (not tlb[i].valid):
				tlb[i] = entry
				return
		# Replace with OPT
		tlb_opt= [0 for i in range(len(tlb))]
		for i in range(len(tlb)):
			for j in range(access_count, len(access_lines)):
				if tlb[i].checkEqual(access_lines[j][0], int(access_lines[j][1]/page_sz)):
					tlb_opt[i] = j
					break
		index = tlb_opt.index(max(tlb_opt))
		tlb[index] = entry

def check_tlb(pid, page_num):
	for i in tlb:
		if (i.valid == True and i.checkEqual(pid, page_num) == True):
			print("TLB hit")
			return True
	print("TLB Miss")
	return False

def check_ram(pid, page_num):
	proc = proc_dict[pid]
	page_entry = proc.ptable[page_num]

	if (page_entry.present == True):
		print("Found at PPN:",page_entry.ppn)
		elem = TLB_Entry()
		elem.insert(pid,page_num,page_entry.ppn)
		insert_tlb(elem)
		return True

	print("PAGE_FAULT")
	return False

def check_kpt(pid, page_num):
	spn = kernel_pt[(pid,page_num)]
	if (ram_pages_free == 0):
		((pid_free,proc_vpn),ram_ind) = mem_toBeFreed()
		# ((pid_free,proc_vpn),ram_ind) = (ram[0], 0)
		proc_dict[pid_free].ptable[proc_vpn].present = False
		proc_dict[pid_free].ptable[proc_vpn].ppn = spn
		swap[spn] = (pid_free,proc_vpn)
		kernel_pt[(pid_free,proc_vpn)] = spn
		for i in tlb:
			if (i.checkEqual(pid_free,proc_vpn)):
				i.valid = False
				break
	else:
		for i in range(len(ram)):
			if (i == None):
				ram_ind = i
				fifo_pr.append(i)
				break
	ram[ram_ind] = (pid,page_num)
	proc_dict[pid].ptable[page_num].present = True
	proc_dict[pid].ptable[page_num].ppn = ram_ind

	elem = TLB_Entry()
	elem.insert(pid,page_num,ram_ind)
	insert_tlb(elem)

def mem_toBeFreed():
	if pr_algo == "FIFO":
		ind = fifo_pr.pop(0)
		fifo_pr.append(ind)
		return (ram[ind],ind)
	elif pr_algo == "LRU":
		ram_lru = [-1 for i in ram]
		for i in range(len(ram)):
			for j in range(access_count-1,-1,-1):
				if ram[i][0] == access_lines[j][0] and ram[i][1] == access_lines[j][1]:
					ram_lru[i] = j
					break
		index = ram_lru.index(min(ram_lru))
		return (ram[index],index)
	elif pr_algo == "OPT":
		ram_opt = [float('inf') for i in ram]
		for i in range(len(ram)):
			for j in range(access_count,len(access_lines)):
				if ram[i][0] == access_lines[j][0] and ram[i][1] == access_lines[j][1]:
					ram_opt[i] = j
					break
		index = ram_opt.index(max(ram_opt))
		return (ram[index],index)

def kill_process(pid):
	global ram_pages_free, swap_pages_free
	for i in tlb:
		if (i.pid == pid):
			i.valid = False
	for i in range(len(ram)):
		if (ram[i] != None and ram[i][0] == pid):
			ram[i] = None
			ram_pages_free += 1
	for i in range(len(swap)):
		if (swap[i] != None and swap[i][0] == pid):
			swap[i] = None
			swap_pages_free += 1
	print("Process ", pid, " killed due to invalid memory access")


def access_mem(pid, address):
	page_num = int(address/page_sz)
    # Segmentation Fault if address greater than virtual space accessed
	if (address+1 > proc_dict[pid].vsize):
		print("ERROR: Segmentation Fault.")
		kill_process(pid)
		return
    
	if (pid in proc_dict):
		if(not check_tlb(pid,page_num)):
			if (not check_ram(pid, page_num)):
				check_kpt(pid,page_num)
	else:
		print("ERROR: No running process with pid: ",pid)

def insert_proc(pid, v_size):
	num_pages = ceil(v_size/page_sz)
	global ram_pages_free, swap_pages_free

	if (num_pages > ram_pages_free + swap_pages_free):
		print("ERROR: Dropping process " + str(pid) + ". Not enough memory.")
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
			fifo_pr.append(i)

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
	ram_numpages = int(ceil(ram_sz/page_sz))
	swap_numpages = int(ceil(swap_sz/page_sz))
	ram = [None for i in range(ram_numpages)]
	swap = [None for i in range(swap_numpages)]
	tlb = [TLB_Entry() for i in range(tlb_size)]
	if tlb_algo == "LRU":
		tlb_lru = [0 for i in range(tlb_size)]
	ram_pages_free = ram_numpages
	swap_pages_free = swap_numpages

	
	# Read Input
	filename1 = "sample inputfile1.txt"
	with open(filename1) as file_obj:
		proc_lines = file_obj.read().split('\n')

	for i in proc_lines:
		k = i.split()
		insert_proc(int(k[0]),int(k[1]))

	# print(ram)
	# print(kernel_pt)

	filename2 = "sample inputfile2.txt"
	with open(filename2) as file_obj:
		access_lines = file_obj.read().strip().split('\n')

	for i in range(len(access_lines)):
		k = access_lines[i].split()
		access_lines[i] = (int(k[0]),int(k[1]))

	
	# print("TEST: ",)
	for i in range(len(access_lines)):
		print("### MEM ACCESS " + str(i) + " PID: " + str(access_lines[i][0]) + " VA: " + str(access_lines[i][1]), " PG: ", int(access_lines[i][1]/page_sz))
		data = access_mem(access_lines[i][0],access_lines[i][1])
		print("TLB: ")
		for i in tlb:
			i.printfn()
		print("RAM: ",ram)
		print("Swap: ",swap)
		access_count+=1
        #print('\n')
		# print(data)
		# for i in tlb:
		# 	i.printfn()
		# print(ram)
		# print('\n')
	# print(access_lines)
	# print(lines)
	# 