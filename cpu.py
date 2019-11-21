"""CPU functionality."""

import sys
class CPU:
    """Main CPU class."""

    def __init__(self, register = [0] * 8, ram = [0] * 256, pc = 0):
        """Construct a new CPU."""
        self.ram = ram
        self.register = register
        self.pc = pc
        self.halted = False
        self.sp = 244 #memory - reserved, vectors and current key press
        self.flag = {'E':0, 'L': 0, 'G': 0}
        self.printouts = []
        #branchtable operations
        OP1 = 0b00000001 #HLT
        OP2 = 0b10000010 #LDI
        OP3 = 0b01000111 #PRN
        OP4 = 0b10100010 #MULTIPLY
        OP5 = 0b01000101 #PUSH
        OP6 = 0b01000110 #POP
        OP7 = 0b01010000 #CALL
        OP8 = 0b00010001 #RET
        OP9 = 0b10100000 #ADD
        OP10 = 0b10100111 #CMP
        OP11 = 0b01010100 #JMP
        OP12 = 0b01010101 #JEQ
        OP13 = 0b01010110 #JNE
        OP14 = 0b01001000 #PRA
        OP15 = 0b10101000 #_and
        OP16 = 0b10101010 #_or
        OP17 = 0b10101011 #_xor

        self.branchtable = {}
        self.branchtable[OP1] = self.HLT
        self.branchtable[OP2] = self.LDI
        self.branchtable[OP3] = self.PRN
        self.branchtable[OP4] = self.multiply
        self.branchtable[OP5] = self.push
        self.branchtable[OP6] = self.pop
        self.branchtable[OP7] = self.call
        self.branchtable[OP8] = self.ret
        self.branchtable[OP9] = self.add
        self.branchtable[OP10] = self.CMP
        self.branchtable[OP11] = self.JMP
        self.branchtable[OP12] = self.JEQ
        self.branchtable[OP13] = self.JNE
        self.branchtable[OP14] = self.PRA
        self.branchtable[OP15] = self._and
        self.branchtable[OP16] = self._or
        self.branchtable[OP17] = self._xor

    def load(self, values):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:
        program = values

        #with open(sys.argv[1]) as f:

        #   for line in f:
        #        line = line.split("#")[0]
        #        line = line.strip()

        #        if line == '':
        #            continue

        #        program.append(int(line, 2))

        print(program)
        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()
    
    def HLT(self):
        self.halted = True
    
    def LDI(self):
        op_a = self.ram_read(self.pc + 1)
        op_b = self.ram_read(self.pc + 2)
        self.register[op_a] = op_b
        self.pc += 3
    
    def PRN(self):
        op_a = self.ram_read(self.pc + 1)
        print(self.register[op_a])
        self.printouts.append(self.register[op_a])
        self.pc += 2
    
    def multiply(self):
        op_a = self.ram_read(self.pc + 1)
        op_b = self.ram_read(self.pc + 2)
        self.register[op_a] *= self.register[op_b]
        self.pc += 3
    
    def pop(self):
        address = self.ram[self.pc + 1]
        self.register[address] = self.ram[self.sp]
        self.sp += 1
        self.pc += 2
    
    def push(self):
        address = self.ram[self.pc + 1]
        self.sp -= 1
        value = self.register[address]
        self.ram[self.sp] = value
        self.pc += 2

    def call(self):
        #stores next address
        self.sp -= 1
        self.ram[self.sp] = self.pc + 2
        #jumps to location in the given register.
        self.pc = self.register[self.ram[self.pc + 1]]

    def ret(self):
        #jumps back to the address stored in the call function.
        self.pc = self.ram[self.sp]
        self.sp += 1

    def add(self):
        op_a = self.ram_read(self.pc + 1)
        op_b = self.ram_read(self.pc + 2)
        self.alu("ADD", op_a, op_b)
        self.pc += 3

    def CMP(self):
        op_a = self.register[self.ram[self.pc + 1]]
        op_b = self.register[self.ram[self.pc + 2]]

        #reset flags to 0
        #seems to work without this
        #self.flag = self.flag.fromkeys(self.flag, 0)

        #sets flag based on comparison of addresses.
        if op_a == op_b:
            self.flag['E'] = 1
        if op_a < op_b:
            self.flag['L'] = 1
        if op_a > op_b:
            self.flag['G'] = 1

        self.pc += 3
    
    def JMP(self):
        #jumps to the address stored in the register.
        address = self.register[self.ram[self.pc + 1]]
        self.pc = address

    def JEQ(self):
        #if the compared values are equal, jump to the stored address.
        if self.flag['E'] == 1:
            self.pc = self.register[self.ram[self.pc +1]]
        else:
            self.pc += 2
    
    def JNE(self):
        #if the compared values are not equal, jump to the stored address.
        if self.flag['E'] == 0:
            self.pc = self.register[self.ram[self.pc + 1]]
        else:
            self.pc += 2
        
    def PRA(self):
        op_a = self.ram_read(self.pc + 1)
        self.printouts.append(str(chr(self.register[op_a])))
        self.pc += 2

    def run(self):
        """Run the CPU."""
        while not self.halted:
            instruction = self.ram[self.pc]
            self.branchtable[instruction]()
        return self.printouts

    def ram_read(self, MAR):
        #Takes in an address in memory and returns the value stored there.
        value = self.ram[MAR]
        return value

    def ram_write(self, MAR, MDR):
        #Accepts an address and value. Writes the value to the given address in memory.
        self.ram[MAR] = MDR
    
    def _and(self):
        op_a = self.ram_read(self.pc+1)
        op_b = self.ram_read(self.pc+2)

        self.register[op_a] = self.register[op_a] & self.register[op_b]
        self.pc += 3

    def _or(self):
        op_a = self.ram_read(self.pc+1)
        op_b = self.ram_read(self.pc+2)
        self.register[op_a] = self.register[op_a] | self.register[op_b]
        self.pc += 3

    def _xor(self):
        op_a = self.ram_read(self.pc+1)
        op_b = self.ram_read(self.pc+2)
        self.register[op_a] = self.register[op_a] ^ self.register[op_b]
        self.pc += 3
