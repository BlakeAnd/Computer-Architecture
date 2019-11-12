"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.register = [0] * 8

    def load(self):
        """Load a program into memory."""

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

        program_name = sys.argv[1]
        address = 0

        with open(program_name) as file:
            for line in file:
                line = line.split('#')[0]
                line = line.strip() #lose whitespace

                if line == '':
                    continue

                val = int(line, 2) #LS-8 uses base 
                # print(val)

                self.ram[address] = val
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

    def LDI(self, register_num, value):
        self.register[register_num] = value
    
    def PRN(self, register_num):
        print(self.register[register_num])

    def MULT(self, reg1, reg2):
        val1 = self.register[reg1]
        val2 = self.register[reg2]
        product = val1*val2
        self.register[reg1] = product


    def ram_read(self, address):
        value = self.ram[address]
        return value

    def ram_write(self, address, value):
        self.ram[address] = value

    def run(self):
        """Run the CPU."""
        address = 0
        HALT = 1
        LDI = 130
        PRN = 71
        MULT = 162
        IR = self.ram_read(address)

        while IR != HALT:
            IR = self.ram_read(address)
            if IR == LDI:
                register = self.ram_read(address+1)
                value = self.ram_read(address+2)
                self.LDI(register, value)
                address += 3
            elif IR == PRN:
                prn_register = self.ram_read(address+1)
                self.PRN(prn_register)
                address += 2
            elif IR == MULT:
                mult_reg1 = self.ram_read(address+1)
                mult_reg2 = self.ram_read(address+2)
                self.MULT(mult_reg1, mult_reg2)
                address += 3

            # print(address, IR)
            


