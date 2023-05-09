from blazeqr.qrlibs.constant import char_cap, required_bytes, mode_index_map, error_correction_level_index_map, num_list, alphanum_list, grouping_list, mode_indicator
       
# dict with encoding functions for each mode
mode_encoding = {
    'numeric': lambda s: numeric_encoding(s),
    'alphanumeric': lambda s: alphanumeric_encoding(s),
    'byte': lambda s: byte_encoding(s),
    'kanji': lambda s: kanji_encoding(s)
}

def encode(ver, ecl, str):
    # determine the best encoding mode and QR code version
    ver, mode = determine_qr_params(ver, ecl, str)
    print('line 16: mode:', mode)
    
    # generate the QR code data
    code = mode_indicator[mode] + get_cci(ver, mode, str) + mode_encoding[mode](str)
    
    # add a terminator
    required_bits = 8 * required_bytes[ver-1][error_correction_level_index_map[ecl]]
    b = required_bits - len(code)
    code += '0000' if b >= 4 else '0' * b
    
    # make the length a multiple of 8
    while len(code) % 8 != 0:
        code += '0'
    
    # add pad bytes if the data is still too short
    while len(code) < required_bits:    
        code += '1110110000010001' if required_bits - len(code) >= 16 else '11101100'
        
    # partition the data into codewords
    data_code = [int(code[i:i+8], 2) for i in range(0, len(code), 8)]
    g = grouping_list[ver-1][error_correction_level_index_map[ecl]]
    data_codewords, i = [], 0
    for n in range(g[0]):
        data_codewords.append(data_code[i:i+g[1]])
        i += g[1]
    for n in range(g[2]):
        data_codewords.append(data_code[i:i+g[3]])
        i += g[3]
    
    return ver, data_codewords
    
def determine_qr_params(ver, ecl, str):
    # determine the best encoding mode and QR code version for the given string
    if all(i in num_list for i in str):
        mode = 'numeric'
    elif all(i in alphanum_list for i in str):
        mode = 'alphanumeric'
    else:
        mode = 'byte'
    
    # find the smallest version that can accommodate the data at the given error correction level
    m = mode_index_map[mode]
    l = len(str)
    for i in range(40):
        if char_cap[ecl][i][m] > l:
            ver = i + 1 if i+1 > ver else ver
            break
 
    return ver, mode

def numeric_encoding(str):   
    # encode numeric data in groups of 3 digits
    str_list = [str[i:i+3] for i in range(0, len(str), 3)]
    code = ''
    for i in str_list:
        rqbin_len = 10
        if len(i) == 1: 
            rqbin_len = 4
        elif len(i) == 2:
            rqbin_len = 7
        code_temp = bin(int(i))[2:]
        code += ('0'*(rqbin_len - len(code_temp)) + code_temp)
    return code
    
def alphanumeric_encoding(str):
    # encode alphanumeric data in groups of 2 characters
    code_list = [alphanum_list.index(i) for i in str]
    code = ''
    for i in range(1, len(code_list), 2):
        c = bin(code_list[i-1] * 45 + code_list[i])[2:]
        c = '0'*(11-len(c)) + c
        code += c
    if i != len(code_list) - 1:
        c = bin(code_list[-1])[2:]
        c = '0'*(6-len(c)) + c
        code += c
    return code
    
def byte_encoding(str):
    # encode byte data using ISO-8859-1 encoding
    code = ''
    for i in str:
        c = bin(ord(i.encode('iso-8859-1')))[2:]
        c = '0'*(8-len(c)) + c
        code += c
    return code
    
def kanji_encoding(str):
    # not yet implemented
    pass
    
def get_cci(ver, mode, str):
    # get the character count indicator for the given version and encoding mode
    if 1 <= ver <= 9:
        cci_len = (10, 9, 8, 8)[mode_index_map[mode]]
    elif 10 <= ver <= 26:
        cci_len = (12, 11, 16, 10)[mode_index_map[mode]]
    else:
        cci_len = (14, 13, 16, 12)[mode_index_map[mode]]
        
    cci = bin(len(str))[2:]
    cci = '0' * (cci_len - len(cci)) + cci
    return cci
    
if __name__ == '__main__':
    # example usage
    s = '123456789'
    v, datacode = encode(1, 'H', s)
    print(v, datacode)