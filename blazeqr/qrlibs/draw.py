from PIL import Image
import numpy as np
import os

def draw_qrcode(abspath, qr_matrix):
    # Set up variables
    unit_len = 3
    x_start = y_start = 4*unit_len
    size = (len(qr_matrix)+8) * unit_len

    # Create image
    pic = Image.new('1', (size, size), 'white')
    np_pic = np.array(pic)

    # Draw QR code
    np_black = np.array([0]*unit_len*unit_len, dtype=np.uint8).reshape(unit_len, unit_len)
    for row, line in enumerate(qr_matrix):
        for col, module in enumerate(line):
            if module:
                x0, y0 = x_start + col * unit_len, y_start + row * unit_len
                x1, y1 = x0 + unit_len, y0 + unit_len
                np_pic[y0:y1, x0:x1] = np_black

    # Save image
    pic = Image.fromarray(np_pic)
    saving = os.path.join(abspath, 'qrcode.png')
    pic.save(saving)
    return saving