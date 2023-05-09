import os
import argparse
from blazeqr.blazeqr import generate_qr

def main():
    # Create an argument parser
    argparser = argparse.ArgumentParser()

    # Define the command-line arguments
    argparser.add_argument('Words', help='The words to produce your QR-code background_image, like a URL or a sentence. Please read the README file for the supported characters.')
    argparser.add_argument('-v', '--version', type=int, choices=range(1, 41), default=1, help='The version means the length of a side of the QR-Code background_image. From little size to large is 1 to 40.')
    argparser.add_argument('-l', '--level', choices=list('LMQH'), default='H', help='Use this argument to choose an Error-Correction-Level: L(Low), M(Medium) or Q(Quartile), H(High). Otherwise, just use the default one: H')
    argparser.add_argument('-p', '--background_image', help='The background_image e.g. example.jpg')
    argparser.add_argument('-c', '--colorized', action='store_true', help="Produce a colorized QR-Code with your background_image. Just works when there is a correct '-p' or '--background_image'.")
    argparser.add_argument('-con', '--contrast', type=float, default=1.0, help='A floating point value controlling the enhancement of contrast. Factor 1.0 always returns a copy of the original image, lower factors mean less color (brightness, contrast, etc), and higher values more. There are no restrictions on this value. Default: 1.0')
    argparser.add_argument('-bri', '--brightness', type=float, default=1.0, help='A floating point value controlling the enhancement of brightness. Factor 1.0 always returns a copy of the original image, lower factors mean less color (brightness, contrast, etc), and higher values more. There are no restrictions on this value. Default: 1.0')
    argparser.add_argument('-n', '--name', help="The filename of output tailed with one of {'.jpg', '.png', '.bmp', '.gif'}. eg. exampl.png")
    argparser.add_argument('-d', '--directory', default=os.getcwd(), help='The directory of output.')

    # Parse the command-line arguments
    args = argparser.parse_args()

    # Print a message if producing a GIF may take a while
    if args.background_image and args.background_image[-4:] == '.gif':
        print('It may take a while, please wait for minutes...')

    # Call the generate_qr function with the provided arguments
    try:
        ver, ecl, qr_name = generate_qr(
            args.Words,
            args.version,
            args.level,
            args.background_image,
            args.colorized,
            args.contrast,
            args.brightness,
            args.name,
            args.directory
        )

        # Print a success message and the path to the QR code
        print('Succeed! \nCheck out your', str(ver) + '-' + str(ecl), 'QR-code:', qr_name)
    except:
        raise