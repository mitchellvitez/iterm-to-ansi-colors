# Converts .itermcolors to colors usable with cygwin. Usage:
# python iterm_to_ansi.py vital.itermcolors >> ~/.minttyrc

import plistlib
import sys

color_names = ['Black', 'Red', 'Green', 'Yellow', 'Blue', 'Magenta', 'Cyan', 'White']
rgb = {'Red': 0, 'Green': 1, 'Blue': 2}

def normalize(value):
    return int(value * 256)

def get_values_255(components):
    values_255 = [0, 0, 0]

    for name, value in components.items():
        for space in rgb:
            if name == space + ' Component':
                values_255[rgb[space]] = normalize(value)

    return values_255

def get_color_name(color_num):
    color_name = ''

    if color_num >= 8:
        color_num %= 8
        color_name += 'Bold'

    color_name += color_names[color_num]

    return color_name

def main():
    if len(sys.argv) < 2:
        print "Please pass in the .itermcolors filename you wish to use"
        sys.exit(-1)

    with open(sys.argv[1]) as iterm_file:
        plist = plistlib.readPlist(iterm_file)

        for color, components in plist.items():
            if not color.startswith('Ansi'):
                continue

            color_name = get_color_name(int(color.split(' ')[1]))

            values_255 = get_values_255(components)
            values_255_string = ','.join(str(x) for x in values_255)
            
            print '{}={}'.format(color_name, values_255_string)

if __name__ == '__main__':
    main()
