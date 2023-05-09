import os
from blazeqr.qrlibs import theqrmodule
from PIL import Image
   
# Positional parameters
#   words: str
#
# Optional parameters
#   version: int, from 1 to 40
#   level: str, just one of ('L','M','Q','H')
#   background_image: str, a filename of a image
#   colorized: bool
#   contrast: float
#   brightness: float
#   save_name: str, the output filename like 'example.png'
#   save_dir: str, the output directory
#
# See [https://github.com/sirmghsbd/blaze] for more details!
def generate_qr(words, version=1, level='H', background_image=None, colorized=False, contrast=1.0, brightness=1.0, save_name=None, save_dir=os.getcwd()):

    """
    Generate QR code with the specified parameters.
    Args:
        words (str): The words to produce the QR code for.
        version (int): The version of the QR code (1 to 40).
        level (str): The error-correction level to use ('L', 'M', 'Q', or 'H').
        background_image (str): The path to an image file to use as the background for the QR code.
        colorized (bool): Whether to colorize the QR code using the background image.
        contrast (float): The contrast enhancement factor to apply to the background image.
        brightness (float): The brightness enhancement factor to apply to the background image.
        save_name (str): The name to use for the output file.
        save_dir (str): The directory to save the output file in.

    Returns:
        A tuple containing the version of the QR code, the error-correction level used, and the path to the output file.
    """

    supported_chars = r"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz ··,.:;+-*/\~!@#$%^&`'=<>[]()?_{}|"


    # Check the validity of the input parameters
    if not isinstance(words, str) or any(i not in supported_chars for i in words):
        raise ValueError('Invalid characters in words! Make sure the characters are supported.')
    if not isinstance(version, int) or version not in range(1, 41):
        raise ValueError('Invalid version! Please choose an integer value from 1 to 40.')
    if not isinstance(level, str) or len(level) > 1 or level not in 'LMQH':
        raise ValueError("Invalid error correction level! Please choose a string value from {'L','M','Q','H'}.")
    if background_image:
        if not isinstance(background_image, str) or not os.path.isfile(background_image) or background_image[-4:] not in ('.jpg', '.png', '.bmp', '.gif'):
            raise ValueError("Invalid background_image! Please input a filename that exists and is tailing with one of {'.jpg', '.png', '.bmp', '.gif'}.")
        if background_image[-4:] == '.gif' and save_name and save_name[-4:] != '.gif':
            raise ValueError('Invalid save_name! If the background_image is in .gif format, the output filename should also be in .gif format.')
        if not isinstance(colorized, bool):
            raise ValueError('Invalid colorized! Please input a boolean value.')
        if not isinstance(contrast, float):
            raise ValueError('Invalid contrast! Please input a float value.')
        if not isinstance(brightness, float):
            raise ValueError('Invalid brightness! Please input a float value.')
    if save_name and (not isinstance(save_name, str) or save_name[-4:] not in ('.jpg', '.png', '.bmp', '.gif')):
        raise ValueError("Invalid save_name! Please input a filename tailing with one of {'.jpg', '.png', '.bmp', '.gif'}.")
    if not os.path.isdir(save_dir):
        raise ValueError('Invalid save_dir! Please input an existing directory.')
    
    # Define the function to combine_qr_background the QR code and the background image    
    def combine_qr_background(ver, qr_name, bg_name, colorized, contrast, brightness, save_dir, save_name=None):
        from blazeqr.qrlibs.constant import alignment_location
        from PIL import ImageEnhance, ImageFilter

        # Load the QR code and the background image
        qr = Image.open(qr_name)
        qr = qr.convert('RGBA') if colorized else qr
        bg0 = Image.open(bg_name).convert('RGBA')
        bg0 = ImageEnhance.Contrast(bg0).enhance(contrast)
        bg0 = ImageEnhance.Brightness(bg0).enhance(brightness)

        # Resize the background image to fit the QR code
        if bg0.size[0] < bg0.size[1]:
            bg0 = bg0.resize((qr.size[0]-24, (qr.size[0]-24)*int(bg0.size[1]/bg0.size[0])))
        else:
            bg0 = bg0.resize(((qr.size[1]-24)*int(bg0.size[0]/bg0.size[1]), qr.size[1]-24))

        # Convert the background image to black and white if not colorized    
        bg = bg0 if colorized else bg0.convert('1')
        
        # Add alignment patterns to the QR code
        alignments = []
        if ver > 1:
            aloc = alignment_location[ver-2]
            for a in range(len(aloc)):
                for b in range(len(aloc)):
                    if not ((a==b==0) or (a==len(aloc)-1 and b==0) or (a==0 and b==len(aloc)-1)):
                        for i in range(3*(aloc[a]-2), 3*(aloc[a]+3)):
                            for j in range(3*(aloc[b]-2), 3*(aloc[b]+3)):
                                alignments.append((i,j))

        for i in range(qr.size[0]-24):
            for j in range(qr.size[1]-24):
                if not ((i in (18,19,20)) or (j in (18,19,20)) or (i<24 and j<24) or (i<24 and j>qr.size[1]-49) or (i>qr.size[0]-49 and j<24) or ((i,j) in alignments) or (i%3==1 and j%3==1) or (bg0.getpixel((i,j))[3]==0)):
                    qr.putpixel((i+12,j+12), bg.getpixel((i,j)))
        
        qr_name = os.path.join(save_dir, os.path.splitext(os.path.basename(bg_name))[0] + '_qrcode.png') if not save_name else os.path.join(save_dir, save_name)
        qr.resize((qr.size[0]*3, qr.size[1]*3)).save(qr_name)
        return qr_name

    tempdir = os.path.join(os.path.expanduser('~'), '.myqr')
    
    # Generate QR code
    try:
        if not os.path.exists(tempdir):
            os.makedirs(tempdir)

        ver, qr_name = theqrmodule.get_qrcode(version, level, words, tempdir)

        if background_image and background_image[-4:]=='.gif':
            import imageio
             
            im = Image.open(background_image)
            duration = im.info.get('duration', 0)
            im.save(os.path.join(tempdir, '0.png'))
            while True:
                try:
                    seq = im.tell()
                    im.seek(seq + 1)
                    im.save(os.path.join(tempdir, '%s.png' %(seq+1)))
                except EOFError:
                    break
            # Combine QR code and each frame of the GIF
            imsname = []
            for s in range(seq+1):
                bg_name = os.path.join(tempdir, '%s.png' % s)
                imsname.append(combine_qr_background(ver, qr_name, bg_name, colorized, contrast, brightness, tempdir))
            # Save the combined frames as a GIF
            ims = [imageio.imread(pic) for pic in imsname]
            qr_name = os.path.join(save_dir, os.path.splitext(os.path.basename(background_image))[0] + '_qrcode.gif') if not save_name else os.path.join(save_dir, save_name)
            imageio.mimwrite(qr_name, ims, '.gif', **{ 'duration': duration/1000 })
        elif background_image:
            # Combine QR code and background image
            qr_name = combine_qr_background(ver, qr_name, background_image, colorized, contrast, brightness, save_dir, save_name)
        elif qr_name:
            # Resize and save the QR code
            qr = Image.open(qr_name)
            qr_name = os.path.join(save_dir, os.path.basename(qr_name)) if not save_name else os.path.join(save_dir, save_name)
            qr.resize((qr.size[0]*3, qr.size[1]*3)).save(qr_name)
          
        return ver, level, qr_name
        
    except:
        raise
    finally:
        # Clean up temporary directory
        import shutil
        if os.path.exists(tempdir):
            shutil.rmtree(tempdir) 