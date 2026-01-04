def parse_register(reg_str):
    return int(reg_str.replace('X', ''))

def get_machine_code(line):
    line = line.strip()
    if not line:
        return None

    clean_line = line.replace(',', ' ').replace('[', ' ').replace(']', ' ').replace('.', ' ')
    parts = clean_line.split()
    
    # Bits 3-4 represent reg_d
    reg_d = parse_register(parts[1]) 
    
    # Bits 0-1 represent reg_one
    reg_one = parse_register(parts[2]) 
    
    last_op_str = parts[3]
    
    is_immediate = False
    
    # Variables for the last input
    reg_two = 0
    imm_val = 0

    if 'X' in last_op_str.upper():
        is_immediate = False
        # Bits 5-6 represent reg_two
        reg_two = parse_register(last_op_str)
    else:
        is_immediate = True
        imm_val = int(last_op_str)

    instruction = 0

    # Setting opcode (Bits 14-15)
    opcode = 0
    if parts[0].upper()  == 'ADD': opcode = 0b00
    elif parts[0].upper()  == 'SUB': opcode = 0b01
    elif parts[0].upper()  == 'LDR': opcode = 0b10
    elif parts[0].upper()  == 'STR': opcode = 0b11
    
    # Shifting opcode to bits 15 and 14
    instruction |= (opcode << 14)

    # Shifts reg_d to positions 3 and 4
    instruction |= (reg_d << 3)
    
    # Shifts reg_one to positions 0 and 1
    instruction |= (reg_one << 0)

    # Setting immediate flag
    if is_immediate:
        # Bit 2: Imm? = 1
        instruction |= (1 << 2)
        
        # Bits 6-13: immediate val
        instruction |= (imm_val << 6)
    else:
        # Bit 2: Imm? = 0
        instruction |= (0 << 2)
        
        # Shifts reg_two to positions 5 and 6
        instruction |= (reg_two << 5)

    return instruction

def write_logisim_file(filename, hex_codes):
    with open(filename, 'w') as f:
        f.write("v3.0 hex words addressed\n")
        
        address = 0
        for i in range(0, len(hex_codes), 16):
            line_prefix = f"{address:02x}: "
            chunk = hex_codes[i:i+16]
            line_content = " ".join(chunk)
            
            f.write(line_prefix + line_content + "\n")
            address += 16 

def process_instructions():
    with open('instr.txt', 'r') as f:
        lines = f.readlines()

    instr_hex = []
    
    for line in lines:
        code = get_machine_code(line)
        if code is not None:
            instr_hex.append(f"{code:04x}")

    instr_hex.append("ffff")
    instr_hex.append("ffff")

    write_logisim_file('instr-img.txt', instr_hex)

def process_data():
    with open('data.txt', 'r') as f:
        content = f.read()

    data_hex = []
    
    content = content.replace('\n', '')
    parts = content.split(',')

    for part in parts:
        part = part.strip()
        if part:
            val = int(part)
            data_hex.append(f"{val:02x}")

    write_logisim_file('data-img.txt', data_hex)

def main():
    process_instructions()
    process_data()

if __name__ == "__main__":
    main()