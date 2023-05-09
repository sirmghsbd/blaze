from PIL import Image
import os

def draw_qrcode(abspath, qrmatrix):
    unit_len = 3
    x = y = 4*unit_len
    size = (len(qrmatrix)+8)*unit_len
    pic = Image.new('1', (size, size), 'white')
    
    for row, line in enumerate(qrmatrix):
        for col, module in enumerate(line):
            if module:
                draw_a_black_unit(pic, x+col*unit_len, y+row*unit_len, unit_len)

    saving = os.path.join(abspath, 'qrcode.png')
    pic.save(saving)
    return saving

def draw_a_black_unit(p, x, y, ul):
    for i in range(ul):
        for j in range(ul):
            p.putpixel((x+i, y+j), 0)
