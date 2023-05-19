from blazeqr.qrlibs.constant import GP_list, ecc_num_per_block, error_correction_level_index_map, po2, log


def encode(ver, error_correction_level, data_codewords):
    """
    Given the version, error correction level, and data codewords, returns the corresponding error correction codewords.

    Args:
        ver (int): The QR code version.
        error_correction_level (str): The error correction level.
        data_codewords (List[int]): The data codewords to encode.

    Returns:
        List[int]: The error correction codewords.
    """
    # Get the number of error correction codewords per block for this version and error correction level.
    ecc_num = ecc_num_per_block[ver-1][error_correction_level_index_map[error_correction_level]]

    # Calculate the error correction codewords for each data codeword.
    ecc = []
    for dc in data_codewords:
        ecc.append(get_ecc(dc, ecc_num))

    return ecc


def get_ecc(dc, ecc_num):
    gp = GP_list[ecc_num]
    remainder = dc
    for i in range(len(dc)):
        remainder = divide(remainder, *gp)
    return remainder
    
def divide(MP, *GP):
    if MP[0]:
        GP = list(GP)
        for i in range(len(GP)):
            GP[i] += log[MP[0]]
            if GP[i] > 255:
                GP[i] %= 255
            GP[i] = po2[GP[i]]
        return XOR(GP, *MP)
    else:
        return XOR([0]*len(GP), *MP)
    
    
def XOR(GP, *MP):
    MP = list(MP)
    a = len(MP) - len(GP)
    if a < 0:
        MP += [0] * (-a)
    elif a > 0:
        GP += [0] * a
    
    remainder = []
    for i in range(1, len(MP)):
        remainder.append(MP[i]^GP[i])
    return remainder