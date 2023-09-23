from pwn import *

# Start the parent process in the background
parent = process("./lab3-3.bin")

# Attach and run as many times as we need
for i in range(3):

        # Open GDB in a new window, attach to the parent, get ready
        # to follow the child once we connect and it forks. Add a
        # breakpoint so we can watch it execute each time.
        gdb.attach(parent, """
        set follow-fork-mode child
        break get_name
        """)

        # If you happen to experience any buggy behavior, add a delay here
        # Sometimes remote() may connect before GDB is attached.
        #        input("Pausing for GDB, press enter to continue... ")

        # Connect to the server, thus forking a child process which GDB will catch
        #p = remote("127.0.0.1", 7033)
        #p.interactive()
