import os

from PIL import Image
import pyperclip


def process_pic_3216(file):
    im = Image.open(file, 'r')
    width, height = im.size
    pic_size_local = int(width * height / 8)
    temp_hex = 0x00
    bit_count = 0
    next_line_count = 0
    output_list = ['{']

    for x in range(0, width):
        for y in range(0, height):
            bit_count += 1
            temp_bin = 1
            for k in im.getpixel((x, y)):
                if k > 125:
                    temp_bin = 0
                    break
            if temp_bin == 1:
                temp_hex |= 0x01
            if bit_count == 8:
                bit_count = 0
                output_list.append("0x%02x" % temp_hex)
                output_list.append(',')
                temp_hex = 0x00
                next_line_count += 1
                if (next_line_count == 16) & ((x != (width - 1)) | (y != (height - 1))):
                    next_line_count = 0
                    output_list.append('\n')
            else:
                temp_hex <<= 1
    output_list.append('}')
    temp = "".join(output_list)
    return temp, pic_size_local


final_list = []
total_pics = 0
pic_size = 0

for file in os.listdir():
    try:
        print(file)
        pic_data, pic_size = process_pic_3216(file)
        final_list.append(pic_data)
        final_list.append(',')
        total_pics += 1
    except IOError:
        continue

final = "\n".join(final_list)
print('[' + str(total_pics) + ']' + '[' + str(pic_size) + ']')
pyperclip.copy(final)
