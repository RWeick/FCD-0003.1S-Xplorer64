import sys
import itertools
import os

def unscramble(addr):
    return (((addr >> 4) & 0x001) | ((addr >> 8) & 0x002) | ((~addr >> 9) & 0x004) | ((addr >> 3) & 0x008) | ((addr >> 6) & 0x010) | ((addr >> 2) & 0x020) | ((~addr << 5) & 0x0C0) | ((~addr << 8) & 0x100) | ((~addr << 6) & 0x200) | ((~addr << 2) & 0x400) | ((addr << 6) & 0x800) | (addr & 0x1F000))

def scramble(addr):
    return (((~addr >> 8) & 0x001) | ((~addr >> 5) & 0x006) | ((~addr >> 6) & 0x008) | ((addr << 4) & 0x010) | ((addr >> 6) & 0x020) | ((addr << 3) & 0x040) | ((addr << 2) & 0x080) | ((~addr >> 2) & 0x100) | ((addr << 8) & 0x200) | ((addr << 6) & 0x400) | ((~addr << 9) & 0x800) | (addr & 0x1F000))

combined_file = open(sys.argv[1], "rb").read()
High = combined_file[::2]
Low = combined_file[1::2]

with open("High.bin", "wb") as High_output:
    High_output.write(High)

with open("Low.bin", "wb") as Low_output:
    Low_output.write(Low)

High_output.close()
Low_output.close()

scrambled_file = open("High.bin", "rb")
unscrambled_file = open("unscrambled_high.bin", "wb")

for i in range(0, 131072):
    
    scrambled_address = scramble(i)
    scrambled_file.seek(scrambled_address)
    unscrambled_byte = scrambled_file.read(1)
    unscrambled_file.write(unscrambled_byte)

scrambled_file.close()
unscrambled_file.close()

scrambled_file = open("Low.bin", "rb")
unscrambled_file = open("unscrambled_low.bin", "wb")

for i in range(0, 131072):
    
    scrambled_address = scramble(i)
    scrambled_file.seek(scrambled_address)
    unscrambled_byte = scrambled_file.read(1)
    unscrambled_file.write(unscrambled_byte)

scrambled_file.close()
unscrambled_file.close()

bufa = bytearray(open("unscrambled_high.bin", "rb").read())
bufb = bytearray(open("unscrambled_low.bin", "rb").read())
open("unscrambled_combined.bin", "wb").write(bytearray(itertools.chain(*zip(bufa, bufb))))

os.remove("high.bin")
os.remove("low.bin")
os.remove("unscrambled_high.bin")
os.remove("unscrambled_low.bin")

