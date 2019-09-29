tlb_algo = "FIFO"
tlb = []
ram = []
swap = []
class Process:
	a = 0

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
			# To do
		elif tlb_algo == "LRU":
			# To Do

# Read Input


# 