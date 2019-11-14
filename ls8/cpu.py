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

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:
        program = []

        with open(sys.argv[1]) as f:

            for line in f:
                line = line.split("#")[0]
                line = line.strip()

                if line == '':
                    continue

                program.append(int(line, 2))

            print(program)
            for instruction in program:
                self.ram[address] = instruction
                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
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
    
    def LDI(self, op_a, op_b):
        self.register[op_a] = op_b
        self.pc += 3
    
    def PRN(self, op_a):
        print(self.register[op_a])
        self.pc += 2
    
    def multiply(self, op_a, op_b):
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

    def run(self):
        """Run the CPU."""
        while not self.halted:
            instruction = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            if instruction == 0b00000001:
                #HLT
                self.HLT()
            
            elif instruction == 0b10000010:
                #LDI
                self.LDI(operand_a, operand_b)
            
            elif instruction == 0b01000111:
                #PRN
                self.PRN(operand_a)

            elif instruction == 0b10100010:
                #MULTIPLY
                self.multiply(operand_a, operand_b)
            
            elif instruction == 0b01000101:
                #PUSH
                self.push()
            
            elif instruction == 0b01000110:
                #POP
                self.pop()

            else:
                pass


    def ram_read(self, MAR):
        #Takes in an address in memory and returns the value stored there.
        value = self.ram[MAR]
        return value

    def ram_write(self, MAR, MDR):
        #Accepts an address and value. Writes the value to the given address in memory.
        self.ram[MAR] = MDR