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

PCB Thickness: 1.2 mm

![image](https://github.com/RWeick/FCD-0003.1S-Xplorer64/blob/main/FCD-0003.1S%20XP64.png)
