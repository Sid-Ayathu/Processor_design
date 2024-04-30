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

pipeline_registers = {
    "IF/ID": {"instruction": "", "pc": 0},
    "ID/EX": {
        "instruction": "",
        "operation": "",
        "rs": "",
        "rt": "",
        "rd": "",
        "shamt": "",
        "imm": "",
        "address": "",
        "instruction_type": "",
    },
    "EX/MEM": {
        "operation": "",
        "offset": 0,
        "ALU_result": 0,
        "instruction": "",
        "imm": 0,
        "is_empty": 1,
    },
    "MEM/WB": {
        "operation": "",
        "rt": "",
        "rd": "",
        "write_val_back": 0,
        "is_empty": 1,
    },
    # creating temporary pipeline registers
    "temp_IF/ID": {"instruction": "", "pc": 0},
    "temp_ID/EX": {
        "instruction": "",
        "operation": "",
        "rs": "",
        "rt": "",
        "rd": "",
        "shamt": "",
        "imm": "",
        "address": "",
        "instruction_type": "",
    },
    "temp_EX/MEM": {
        "operation": "",
        "offset": 0,
        "ALU_result": 0,
        "instruction": "",
        "imm": 0,
        "is_empty": 1,
    },
    "temp_MEM/WB": {
        "operation": "",
        "rt": "",
        "rd": "",
        "write_val_back": 0,
        "is_empty": 1,
    },
}


def Instruction_Fetch(pc):
    i = int((pc - start) / 4)
    if i < len(binary_code):
        instruction = binary_code[i]
        pipeline_registers["temp_IF/ID"] = {"instruction": instruction, "pc": pc}
        return pc + 4
    else:
        # Handle the case when 'i' is out of range (end of program)
        return end_of_program_pc


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

    if instruction_type != "":
        pipeline_registers["temp_ID/EX"] = {
            "operation": operation,
            "rs": rs,
            "rt": rt,
            "rd": rd,
            "shamt": shamt,
            "imm": imm,
            "address": address,
            "instruction_type": instruction_type,
        }

    # return operation, rs, rt, rd, shamt, imm, address, instruction_type


def Execute(pipeline_registers):
    ex_register = pipeline_registers["ID/EX"]
    operation = ex_register["operation"]
    rs = ex_register["rs"]
    rt = ex_register["rt"]
    rd = ex_register["rd"]
    rd = ex_register["rd"]
    shamt = ex_register["shamt"]
    imm = ex_register["imm"]
    address = ex_register["address"]

    offset, ALU_result = Execution(operation, rs, rt, shamt, imm, address)
    pipeline_registers["temp_EX/MEM"] = {
        "operation": operation,
        "offset": offset,
        "ALU_result": ALU_result,
        "rs": rs,
        "rt": rt,
        "rd": rd,
        "is_empty": 0,
    }


data_memory = {j: 0 for j in range(268501168, 268501168 + 4 * 501, 4)}


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


def Memory_Access(pipeline_registers):
    mem_register = pipeline_registers["EX/MEM"]
    # print("EX/MEM:", mem_register)  # Add this line
    operation = pipeline_registers["ID/EX"]["operation"]
    rt = pipeline_registers["ID/EX"]["rt"]
    rd = pipeline_registers["ID/EX"]["rd"]
    offset = mem_register["offset"]

    if operation == "lw":
        register_values[rt] = data_memory[offset]
        pipeline_registers["MEM/WB"] = {"operation": operation, "rt": rt, "rd": rd}
    if operation == "sw":
        data_memory[offset] = register_values[rt]
        pipeline_registers["MEM/WB"] = {"operation": operation, "rt": rt, "rd": rd}

    # pipeline_registers["MEM/WB"] = {"operation": operation, "rt": rt, "rd": rd}
    # print("MEM/WB:", pipeline_registers["MEM/WB"])  # Add this line


def Writeback(pipeline_registers):
    wb_register = pipeline_registers["MEM/WB"]

    if "operation" in wb_register:
        operation = wb_register["operation"]
        rt = wb_register["rt"]
        rd = wb_register["rd"]
        temp1 = pipeline_registers["EX/MEM"]["ALU_result"]

        if operation in {"add", "addu", "sub", "and", "or", "nor", "slt", "sll", "srl"}:
            register_values[rd] = temp1
        if operation in {"addi", "slti", "andi", "ori"}:
            register_values[rt] = temp1


def forwarding(pipeline_registers):
    wb_register = pipeline_registers["MEM/WB"]
    mem_register = pipeline_registers["EX/MEM"]
    ex_register = pipeline_registers["ID/EX"]
    rs_val = register_values[rs]
    rt_val = register_values[rt]

    rt = ex_register["rt"]
    rs = ex_register["rs"]
    if wb_register["is_empty"] != 1:
        frwd_rd = wb_register["rd"]
        if rt == frwd_rd:
            rt_val = wb_register["write_back_val"]

        if rs == frwd_rd:
            rs_val = wb_register["write_back_val"]

    if mem_register["is_empty"] != 1:
        frwd_rd = mem_register["rd"]
        if rt == frwd_rd:
            rt_val = wb_register["write_back_val"]

        if rs == frwd_rd:
            rs_val = wb_register["write_back_val"]
        if mem_register["operation"] == "lw":
            shd_continue = 1


fp = open("dump3", "r")
binary_code = fp.readlines()
clock_cycles = 0
global pc
pc = 4194380
Clock_cycles = 115
global i
i = 0
global start
start = 4194380
end_of_program_pc = 4194460
Data_memory = []

number_of_intgers = int(input("Enter number of integers: "))
input_address = int(input("Enter input_address: "))
output_address = int(input("Enter output_address: "))
register_values["01001"] = number_of_intgers
register_values["01010"] = input_address
register_values["01011"] = output_address

for j in range(0, number_of_intgers):
    number = int(input("Enter integer: "))
    data_memory[input_address + 4 * j] = number
    Data_memory.append(number)
# first 4 clk cycles hardcode
# 1
pc = Instruction_Fetch(pc)

clock_cycles += 1

# 2
Instruction_Decode(pipeline_registers["IF/ID"]["instruction"])
pc = Instruction_Fetch(pc)

clock_cycles += 1

# 3
Execute(pipeline_registers)
Instruction_Decode(pipeline_registers["IF/ID"]["instruction"])
Data_memory.sort()
pc = Instruction_Fetch(pc)

clock_cycles += 1

# 4
Memory_Access(pipeline_registers)
Execute(pipeline_registers)
Instruction_Decode(pipeline_registers["IF/ID"]["instruction"])
pc = Instruction_Fetch(pc)

clock_cycles += 1

while pc != end_of_program_pc:
    # Pipeline stages
    Writeback(pipeline_registers)
    Memory_Access(pipeline_registers)
    global shd_continue
    shd_continue = 0
    global shd_flush
    shd_flush = 0
    Execute(pipeline_registers)
    if shd_continue == 1:
        continue
    if shd_flush == 1:
        pipeline_registers["IF/ID"] = {}
        pipeline_registers["ID/EX"] = {}
        decimal_value_imm = pipeline_registers["EX/MEM"]["imm"]
        pc = pc + (4 * decimal_value_imm)
        continue
    Instruction_Decode(pipeline_registers["IF/ID"]["instruction"])
    pc = Instruction_Fetch(pc)
    clock_cycles += 1


# hard code last 4

# 4
Writeback(pipeline_registers)
Memory_Access(pipeline_registers)
Execute(pipeline_registers)
Instruction_Decode(pipeline_registers["IF/ID"]["instruction"])

clock_cycles += 1

# 3
Writeback(pipeline_registers)
Memory_Access(pipeline_registers)
Execute(pipeline_registers)

clock_cycles += 1

# 2
Writeback(pipeline_registers)
Memory_Access(pipeline_registers)

# 1
Writeback(pipeline_registers)

clock_cycles += 1

print(f"number of clock cycles = {clock_cycles*6}")

for i in range(0, number_of_intgers):
    print(Data_memory[i])

fp.close()
