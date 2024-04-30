register_values = {
    "00000": 0,
    "00001": 0,
    "00010": 0,
    "00011": 0,
    "00100": 0,
    "00101": 0,
    "00110": 0,
    "00111": 0,
    "01000": 0,
    "01001": 0,
    "01010": 0,
    "01011": 0,
    "01100": 0,
    "01101": 0,
    "01110": 0,
    "01111": 0,
    "10000": 0,
    "10001": 0,
    "10010": 0,
    "10011": 0,
    "10100": 0,
    "10101": 0,
    "10110": 0,
    "10111": 0,
    "11000": 0,
    "11001": 0,
    "11010": 0,
    "11011": 0,
    "11100": 0,
    "11101": 0,
    "11110": 0,
    "11111": 0,  # $ra register value
}


def Instruction_Decode(instruction):
    # Decoding the instruction
    opcode = instruction[0:6]

    instruction_type = ""
    operation = ""
    function = ""
    rs = ""
    rt = ""
    rd = ""
    shamt = ""
    imm = ""
    address = ""

    if opcode == "000000":
        instruction_type = "R"
    if (
        opcode == "000100"
        or opcode == "000101"
        or opcode == "001000"
        or opcode == "001001"
        or opcode == "001010"
        or opcode == "001100"
        or opcode == "001101"
        or opcode == "100011"
        or opcode == "101011"
    ):
        instruction_type = "I"
    if opcode == "000010" or opcode == "000011":
        instruction_type = "J"

    if instruction_type == "R":
        rs = instruction[6:11]
        rt = instruction[11:16]
        rd = instruction[16:21]
        shamt = instruction[21:26]
        function = instruction[26:32]
        if function == "100000":
            operation = "add"
        if function == "100001":
            operation = "addu"
        if function == "100010":
            operation = "sub"
        if function == "100100":
            operation = "and"
        if function == "100101":
            operation = "or"
        if function == "100111":
            operation = "nor"
        if function == "101010":
            operation = "slt"
        if function == "000000":
            operation = "sll"
        if function == "000010":
            operation = "srl"

    elif instruction_type == "I":
        rs = instruction[6:11]
        rt = instruction[11:16]
        imm = instruction[16:32]

        if opcode == "000100":
            operation = "beq"
        if opcode == "000101":
            operation = "bne"
        if opcode == "000111":
            operation = "bgtz"
        if opcode == "001000":
            operation = "addi"
        if opcode == "001001":
            operation = "addiu"
        if opcode == "001010":
            operation = "slti"
        if opcode == "001100":
            operation = "andi"
        if opcode == "001101":
            operation = "ori"
        if opcode == "100011":
            operation = "lw"
        if opcode == "101011":
            operation = "sw"

    elif instruction_type == "J":
        address = instruction[6:32]
        if opcode == "000010":
            operation = "j"
        if opcode == "000011":
            operation = "jal"

    return operation, rs, rt, rd, shamt, imm, address, instruction_type


def Execution(operation, rs, rt, shamt, imm, address):
    global pc
    offset = ""
    temp1 = ""
    start = 4194380
    thirtytwo_address = ""

    if (
        operation == "beq"
        or operation == "bne"
        or operation == "bgtz"
        or operation == "addi"
        or operation == "slti"
        or operation == "andi"
        or operation == "ori"
        or operation == "lw"
        or operation == "sw"
    ):
        # Check if the leftmost bit is 1, indicating a negative number in two's complement
        if imm[0] == "1":
            # Calculate the two's complement value
            inverted_str = "".join("0" if bit == "1" else "1" for bit in imm)
            inverted_value = int(inverted_str, 2)
            decimal_value_imm = -(
                (inverted_value + 1) & 0xFFFF
            )  # Ensure it's a 16-bit value
        if imm[0] == "0":
            # If the leftmost bit is 0, it's a positive number
            decimal_value_imm = int(imm, 2)
    # executing instruction: ALU
    if operation == "add":
        temp1 = register_values[rs] + register_values[rt]
    if operation == "addu":
        temp1 = register_values[rs] + register_values[rt]
    if operation == "sub":
        temp1 = register_values[rs] - register_values[rt]
    if operation == "and":
        temp1 = register_values[rs] & register_values[rt]
    if operation == "or":
        temp1 = register_values[rs] | register_values[rt]
    if operation == "nor":
        temp1 = (~register_values[rs]) & (~register_values[rt])
    if operation == "slt":  # source2 == rt
        if register_values[rs] < register_values[rt]:
            temp1 = 1
        else:
            temp1 = 0
    if operation == "sll":
        temp1 = register_values[rs] << int(shamt, 2)
    if operation == "srl":
        temp1 = register_values[rs] >> int(shamt, 2)

    if operation == "beq":
        if register_values[rs] == register_values[rt]:
            pc = pc + (4 * decimal_value_imm) + 4
        else:
            pc = pc + 4
        # print(f"beq succesful with pc value {pc}")
    if operation == "bne":
        if register_values[rs] != register_values[rt]:
            pc = pc + (4 * decimal_value_imm) + 4
        else:
            pc = pc + 4
        # print(f"bne succesful with pc value {pc}")
    if operation == "bgtz":
        if register_values[rs] > register_values[rt]:
            pc = pc + (4 * decimal_value_imm) + 4
        else:
            pc = pc + 4
    if operation == "addi":
        temp1 = register_values[rs] + decimal_value_imm
    if operation == "slti":
        if register_values[rs] < decimal_value_imm:
            temp1 = 1
        else:
            temp1 = 0
    if operation == "andi":
        temp1 = register_values[rs] & decimal_value_imm
    if operation == "ori":
        temp1 = register_values[rs] | decimal_value_imm
    if operation == "lw":
        offset = register_values[rs] + decimal_value_imm
    # print(decimal_value_imm)
    if operation == "sw":
        offset = register_values[rs] + decimal_value_imm

    if operation == "j":
        thirtytwo_address = "0000" + address + "00"
        # print(thirtytwo_address)
        pc = int(thirtytwo_address, 2)
        # print(f"j succesful with pc value {pc}")

    return offset, temp1


# defining data memory
data_memory = {j: 0 for j in range(268501168, 268501168 + 4 * 501, 4)}


def Mem_read(operation, rt, offset):
    if operation == "lw":
        register_values[rt] = data_memory[offset]
        # print(f"lw succesful with {rt} value {register_values[rt]}")
    if operation == "sw":
        data_memory[offset] = register_values[rt]


def Writeback(operation, rt, rd, temp1):
    if (
        operation == "add"
        or operation == "addu"
        or operation == "sub"
        or operation == "and"
        or operation == "or"
        or operation == "nor"
        or operation == "slt"
        or operation == "sll"
        or operation == "srl"
    ):
        register_values[rd] = temp1
        # print(f"operation {operation} succesful with {rd} value {register_values[rd]}")
    if (
        operation == "addi"
        or operation == "slti"
        or operation == "andi"
        or operation == "ori"
    ):
        register_values[rt] = temp1
        # print(f"operation {operation} succesful with {rt} value {register_values[rt]}")


fp = open("dump3", "r")
binary_code = fp.readlines()
clock_cycles = 0
global pc  # why is it this number =>address of the first instruction in our mips program
pc = 4194380
i = 0
start = 4194380
# taking input
number_of_intgers = int(input("Enter number of integers: "))
input_address = int(input("Enter input_address: "))
output_address = int(input("Enter output_address: "))
register_values["01001"] = number_of_intgers
register_values["01010"] = input_address
register_values["01011"] = output_address

for j in range(0, number_of_intgers):
    number = int(input("Enter integer: "))
    data_memory[input_address + 4 * j] = number

while True:
    # reading in the machine code of instructions one after the oher
    instruction = binary_code[i]

    (
        operation,
        rs,
        rt,
        rd,
        shamt,
        immediate,
        address,
        instruction_type,
    ) = Instruction_Decode(instruction)

    offset, ALU_result = Execution(operation, rs, rt, shamt, immediate, address)

    Mem_read(operation, rt, offset)

    Writeback(operation, rt, rd, ALU_result)

    clock_cycles += 1

    if operation != "j" and operation != "beq" and operation != "bne":
        pc += 4
    i = int((pc - start) / 4)

    if pc > 4194460:
        break
fp.close()
output_address = input_address
# output
print(f"number of clock cycles = {clock_cycles*5}")

for i in range(0, number_of_intgers):
    print(data_memory[output_address + 4 * i])
print(data_memory)
# input address=268501168 or try 268435456
# output address- 268501868 or try 268435856
# data mem start- 268,501,168
