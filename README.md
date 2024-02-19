# FCD-0003.1S-Xplorer64
Firmware, Schematic and Kicad PCB files for the Future Console Design Xplorer64. 

FCD implemented an address scrambling function in their CPLD in order to obfuscate the firmware. An unscrambled firmware is supplied and when it passes through the CPLD to be written to the eeproms, the data is scrambled and unrecognizable. With some analysis, I found a pattern in the scrambled firmware and was able to match it to originating locations in the unscrambled firmware. Many thanks to @Parasyte for deducing the scramble algorithm from that dataset. Firmware can now be scrambled and unscrambled at will using these functions:

function unscramble(addr) {
  return (( addr >> 4) & 0x001) |
         (( addr >> 8) & 0x002) |
         ((~addr >> 9) & 0x004) |
         (( addr >> 3) & 0x008) |
         (( addr >> 6) & 0x010) |
         (( addr >> 2) & 0x020) |
         ((~addr << 5) & 0x0c0) |
         ((~addr << 8) & 0x100) |
         ((~addr << 6) & 0x200) |
         ((~addr << 2) & 0x400) |
         (( addr << 6) & 0x800) |
         (addr & 0x1f000);
}

function scramble(addr) {
  return ((~addr >> 8) & 0x001) |
         ((~addr >> 5) & 0x006) |
         ((~addr >> 6) & 0x008) |
         (( addr << 4) & 0x010) |
         (( addr >> 6) & 0x020) |
         (( addr << 3) & 0x040) |
         (( addr << 2) & 0x080) |
         ((~addr >> 2) & 0x100) |
         (( addr << 8) & 0x200) |
         (( addr << 6) & 0x400) |
         ((~addr << 9) & 0x800) |
         (addr & 0x1f000);
}

Both scrambled and unscrambled firmwares are available in this repository.

I have included python scripts to automate the scramble and unscramble process. Usage is: py scramble.py <file.bin> and py unscramble.py <file.bin>
These will output a single file that is the result of the scrambling/unscrambling.

The entire firmware is mapped to 0x10400000 - 0x1043FFFF and can be easily read out with a Sanni Cart Reader at those addresses. Reading it out this way will produce an unscrambled firmware.

Writing firmware back requires the addresses and data to be transformed according to the scramble/unscramble functions listed above, and requires a read of 0x10760000 to initiate an even address write, or a read of 0x10770000 to initiate an odd address write, followed by the respective write to the transformed address, and ending with a read to 0x10740000. Even and odd writes are determined by dividing the original address in half, right shifting that data by 4, and checking parity. I've implemented this fully in the Sanni Cart Reader, and it can now program Xplorer 64 cartridges.

The parallel port comms are monitored at n64 PI address 0x1030_0000 and the default (nothing happening) data the xplorer 64 sees when nothing is connected to the parallel port is 0x0300_0300.

PCB Thickness: 1.2 mm

![image](https://github.com/RWeick/FCD-0003.1S-Xplorer64/blob/main/FCD-0003.1S%20XP64.png)
