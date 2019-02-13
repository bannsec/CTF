#!/usr/bin/env python

import angr
proj = angr.Project('./obfusc8_much')

# This will house our stack variable address later
failed_addr = None

# Custom avoid lambda
def avoid(s):
    global failed_addr
    
    # Haven't found the stack address yet
    if failed_addr == None:
        return False

    # Avoid states we cannot satisfy (i.e.: they have already set failed_addr to true)
    if not s.satisfiable(extra_constraints=(s.mem[failed_addr].dword.resolved == 0,)):
        print("Pruning state at: {}".format(s.ip))
        return True

    return False

# We simply use this hook to grab the stack address for our fail location
@proj.hook(0x004005b6)
def assert_dont_fail(s):
    global failed_addr
    failed_addr = s.regs.rbp-0x14

# Where we saw the printf call in the binary
printf_call = 0x005c2ad8

# Creating our base state with unicorn (for speed).
state = proj.factory.entry_state(add_options=angr.options.unicorn)

# Manually increasing our symbolic bytes size as the flag is longer than angr normally allows
state.libc.buf_symbolic_bytes = 100

# To save memory, automatically drop any path we avoided
simgr = proj.factory.simgr(state, auto_drop=set(['avoid']))

# To save memory, using Spiller technique
simgr.use_technique(angr.exploration_techniques.Spiller())

# For peace of mind, adding MemoryWatcher to stop us if we're about to run out of space
simgr.use_technique(angr.exploration_techniques.MemoryWatcher())

# Run it!
simgr.explore(find=printf_call, avoid=avoid)

# Print the flag
print(simgr.found[0].posix.dumps(0))
