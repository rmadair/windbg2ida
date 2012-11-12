from sys import exit, argv
import re


def parseFile(filename):
	''' Find all matching patterns in the provided file of registries and the associated comment. Return a dict '''

	pattern = "eax=([0-9a-z]{8}) ebx=([0-9a-z]{8}) ecx=([0-9a-z]{8}) edx=([0-9a-z]{8}) esi=([0-9a-z]{8}) edi=([0-9a-z]{8})[^\n]*\neip=([0-9a-z]{8}) esp=([0-9a-z]{8}) ebp=([0-9a-z]{8})[^\n]*\n[^\n]*\n[^\n]*\n(.*)"
	pattern = re.compile(pattern)
	text = open(filename).read()
	matches = re.findall(pattern, text)
	
	ret = []
	for match in matches:
		eax, ebx, ecx, edx, esi, edi, eip, esp, ebp, last_line = match
		ret.append( {'eax':eax, 'ebx':ebx, 'ecx':ecx, 'edx':edx, 'esi':esi, 'edi':edi, 'esp':esp, 'ebp':ebp, 'last_line':last_line} )
	return ret

def fillInGraph(matches):
	''' Color each instruction, comment the value of the operands '''

	regs_pattern = '(eax|ebx|ecx|edx|esi|edi|esp|ebp)'
	regs_pattern = re.compile(regs_pattern)

	for match in matches:
		# the new comment
		comment = ""

		# the registers used in the instruction
		regs = re.findall(regs_pattern, match['last_line'])
		for reg in regs:
			comment += "%s=%s;" % (reg, match[reg])

		# we are interested in the address and the comment of the last line
		last_line = match['last_line'].split()
		addr = int(last_line[0], 16)
		if len(last_line) > 4:
			if comment:
				comment += '*'+last_line[-1].split(':')[-1]
			else:
				comment += last_line[-1].split(':')[-1]

		# color and comment
		SetColor(addr, CIC_ITEM, 0x7f0000) # blue
		if comment:
			MakeComm(addr, comment)

if __name__ == '__main__':
	# parse the file
	matches = parseFile(argv[1])
	if not matches:
		print 'Unable to parse the file. Exiting'
		exit(1)

	# fill in the info
	fillInGraph(matches)

