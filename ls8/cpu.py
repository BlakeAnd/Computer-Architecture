"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.register = [0] * 8
        self.FL = [0] * 8
        self.address = 0

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
        self.reg_stackpointer = self.register[7]
        self.reg_stackpointer = 0xf4

        self.L = 0 #self.FL[5]
        self.G = 0 #self.FL[6]
        self.E = 0 #self.FL[7]

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "CMP":
            if reg_a > reg_b:
                self.G = 1
                self.L = 0
                self.E = 0
            elif reg_a < reg_b:
                self.G = 0
                self.L = 1
                self.E = 0
            elif reg_a == reg_b:
                self.G = 0
                self.L = 0
                self.E = 1

            self.address += 3

        else:
            raise Exception("Unsupported ALU operation")

    def CMP(self):
        op = "CMP"
        rega = self.register[self.ram_read(self.address+1)]
        regb = self.register[self.ram_read(self.address+2)]
        self.alu(op, rega, regb)

    def JMP(self):
        self.address = self.register[self.ram_read(self.address+1)]
        # self.address += 2

    def JEQ(self):
        if self.E == 1:
            self.JMP()
        else:
            self.address += 2

    def JNE(self):
        # if self.E == 0:
        #     self.address = self.register[self.ram_read(self.address+1)]
        # self.address += 2
        if self.E == 0:
            self.JMP()
        else:
            self.address += 2

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

    def LDI(self):
        register = self.ram_read(self.address+1)
        value = self.ram_read(self.address+2)
        self.register[register] = value
        self.address += 3
    
    def PRN(self):
        prn_register = self.ram_read(self.address+1)        
        print(self.register[prn_register])
        self.address += 2

    def MULT(self):
        reg1 = self.ram_read(self.address+1)
        reg2 = self.ram_read(self.address+2) 
        # print(reg1, reg2)      
        val1 = self.register[reg1]
        val2 = self.register[reg2]
        product = val1*val2
        self.register[reg1] = product
        self.address += 3

    def PUSH(self):
        self.reg_stackpointer -= 1
        register = self.ram_read(self.address+1)
        value = self.register[register]
        self.ram_write(self.reg_stackpointer, value)
        self.address += 2
    
    def POP(self):
        value = self.ram_read(self.reg_stackpointer)
        register = self.ram_read(self.address+1)
        self.register[register] = value
        self.reg_stackpointer += 1
        self.address += 2

    def CALL(self):
        #push the return address on to the stack
        return_address = self.address + 2
        self.reg_stackpointer -= 1
        self.ram_write(self.reg_stackpointer, return_address)

        # set the program address to the value in the register
        register = self.ram_read(self.address+1)
        self.address = self.register[register]

    def RET(self):
        # pop the return address off stack
        # store it in the pc
        self.address = self.ram_read(self.reg_stackpointer)
        self.reg_stackpointer += 1

    def ADD(self):
        reg1 = self.ram_read(self.address+1)
        reg2 = self.ram_read(self.address+2)
        val1 = self.register[reg1]
        val2 = self.register[reg2]
        sum = val1 + val2
        self.register[reg1] = sum
        self.address += 3


    def ram_read(self, address):
        value = self.ram[address]
        return value

    def ram_write(self, address, value):
        self.ram[address] = value

    def run(self):
        """Run the CPU."""
        HALT = 1
        # LDI = 130
        # PRN = 71
        # MULT = 162
        IR = self.ram_read(0)

        table = {
            130: self.LDI, 
            71: self.PRN,
            162: self.MULT,
            0b01000101: self.PUSH,
            0b01000110: self.POP, 
            0b01010000: self.CALL, 
            0b00010001: self.RET,
            160: self.ADD,
            0b10100111: self.CMP,
            0b01010100: self.JMP,
            0b01010101: self.JEQ,
            0b01010110: self.JNE,
        }

        while IR != HALT:
            # print("address", self.address, "val", self.ram_read(self.address))
            # print("address", self.address, "val", IR)
            table[IR]()
            IR = self.ram_read(self.address)
            


