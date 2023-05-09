from blazeqr.qrlibs.constant import required_remainder_bits, error_correction_level_index_map, grouping_list


def structure_final_bits(ver: int, ecl: str, data_codewords: list, ecc: list) -> str:
    """Interleaves data codewords and error correction codewords to form the final bit sequence.

    Args:
        ver (int): The QR code version.
        ecl (str): The error correction level.
        data_codewords (list): A list of data codewords.
        ecc (list): A list of error correction codewords.

    Returns:
        str: The final bit sequence.
    """
    # Interleave data codewords and error correction codewords
    final_message = interleave_dc(data_codewords, ver, ecl) + interleave_ecc(ecc)
    
    # Convert to binary and add remainder bits if necessary
    final_bits = ''.join(['0'*(8-len(i))+i for i in [bin(i)[2:] for i in final_message]]) + '0' * required_remainder_bits[ver-1]
    
    return final_bits


def interleave_dc(data_codewords: list, ver: int, ecl: str) -> list:
    """Interleaves data codewords.

    Args:
        data_codewords (list): A list of data codewords.
        ver (int): The QR code version.
        ecl (str): The error correction level.

    Returns:
        list: The interleaved data codewords.
    """
    interleaved_data = []
    for t in zip(*data_codewords):
        interleaved_data += list(t)
    
    # Add the last bit of each row for rectangular QR codes
    g = grouping_list[ver-1][error_correction_level_index_map[ecl]]
    if g[3]:
        for i in range(g[2]):
            interleaved_data.append(data_codewords[i-g[2]][-1])
    
    return interleaved_data
    

def interleave_ecc(ecc: list) -> list:
    """Interleaves error correction codewords.

    Args:
        ecc (list): A list of error correction codewords.

    Returns:
        list: The interleaved error correction codewords.
    """
    interleaved_ecc = []
    for t in zip(*ecc):
        interleaved_ecc += list(t)

    return interleaved_ecc