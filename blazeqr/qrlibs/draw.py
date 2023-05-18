from PIL import Image
import os

def draw_qrcode(abspath, qr_matrix):
    # Set up variables
    unit_len = 3
    x_start = y_start = 4*unit_len
    size = (len(qr_matrix)+8) * unit_len

    # Create image
    pic = Image.new('1', (size, size), 'white')
    
    # Draw QR code
    for row, line in enumerate(qr_matrix):
        for col, module in enumerate(line):
            if module:
                draw_black_unit(pic, x_start + col * unit_len, y_start + row * unit_len, unit_len)

    # Save image
    saving = os.path.join(abspath, 'qrcode.png')
    pic.save(saving)
    return saving

def draw_black_unit(image, x, y, unit_len):
    # Draw a black square for a single QR code module
    for i in range(unit_len):
        for j in range(unit_len):
            image.putpixel((x+i, y+j), 0)