# -*- coding: utf-8 -*-

from blazeqr.qrlibs import data, ECC, structure, matrix, draw

# ver: Version from 1 to 40
# error_correction_level: Error Correction Level (L,M,Q,H)
# get a qrcode background_image of 3*3 pixels per module
def get_qrcode(ver, error_correction_level, str, save_place):
    # Data Coding
    ver, data_codewords = data.encode(ver, error_correction_level, str)

    # Error Correction Coding
    ecc = ECC.encode(ver, error_correction_level, data_codewords)
    
    # Structure final bits
    final_bits = structure.structure_final_bits(ver, error_correction_level, data_codewords, ecc)
    
    # Get the QR Matrix
    qrmatrix = matrix.get_qrmatrix(ver, error_correction_level, final_bits)
        
    # Draw the background_image and Save it, then return the real ver and the absolute name
    return ver, draw.draw_qrcode(save_place, qrmatrix)
