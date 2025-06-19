# This script cleans .rodata by removing all non-printable and non-ASCII characters.
# It preserves only printable ASCII (0x20–0x7E), newlines, and tabs.

input_path = 'resources/.rodata'
output_path = 'resources/.rodata.cleaned.txt'

with open(input_path, 'rb') as infile, open(output_path, 'wb') as outfile:
    for line in infile:
        cleaned = bytearray()
        for b in line:
            if b == 0x09 or b == 0x0A or (0x20 <= b <= 0x7E):
                cleaned.append(b)
        outfile.write(cleaned)
