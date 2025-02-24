
import sys, struct

def pad_with_zeros(s):
    return s.ljust(16, '0')

def hex_to_little_endian(hex_value):
    byte_value = bytes.fromhex(hex_value)
    little_endian_bytes = byte_value[::-1]
    little_endian_hex = little_endian_bytes.hex()
    
    return little_endian_hex


def count_lines(filename):
    with open(filename, 'r') as file:
        count = sum(1 for _ in file)
    return count

def convert_binary_to_hashes(input_file, output_file):
    print("converting to hashes textfile...")
    with open(input_file, 'rb') as f_in, open(output_file, 'w') as f_out:
        f_in.read(16)
        while (chunk := f_in.read(16)): 
            hash_hex = chunk.hex()
            f_out.write(hash_hex)
            f_out.write("\n")

def convert_hashes_to_binary(input_file, output_file):
    with open(input_file, 'r') as f_in, open(output_file, 'wb') as f_out:
        print("Counting hashes...")
        alllines = count_lines(input_file)
        print(f"Number of hashes: {alllines}")
        lines=hex(alllines)[2:]
        if len(lines) % 2 != 0:  
            lines = '0' + lines  
        lines=hex_to_little_endian(lines)
        lines=pad_with_zeros(lines)
        hash_bytes = bytes.fromhex(lines)
        f_out.write(hash_bytes)
        count = 0
        next_threshold = 10
        for count, line in enumerate(f_in, 1):
            percentage_complete = count / alllines * 100
            if percentage_complete >= next_threshold:
                print(f"Converting hash {count} of {alllines} - {next_threshold}% complete")
                next_threshold += 10
            hash_hex = line.strip()[:32] 
            hash_bytes = bytes.fromhex(hash_hex)
            f_out.write(hash_bytes)


def main():
    if len(sys.argv) != 4:
        print("Usage: python script.py <to-bin|to-text> <inputfile> <outputfile>")
        return

    operation = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]

    if operation == "to-text":
        convert_binary_to_hashes(input_file, output_file)
    elif operation == "to-bin":
        convert_hashes_to_binary(input_file, output_file)
    else:
        print(f"Unknown operation: {operation}. Use 'to-bin' or 'to-text'.")

if __name__ == "__main__":
    main()
