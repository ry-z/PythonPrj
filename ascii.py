from PIL import Image
import argparse

ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")



parser = argparse.ArgumentParser()

#parser.add_argument('file')
#parser.add_argument('-o','--output')#output file
#parser.add_argument('--width',type=int,default=80)
#parser.add_argument('--hright',type=int,default=80)

#args = parser.parse_args()

#IMG = args.file
#WIDTH = args.width
#HEIGHT = args.height
#OUTPUT = args.output

def get_char(r,g,b,alpha = 256):
    if alpha == 0:
        return ' '
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
    lenth = len(ascii_char)
    unit = (256.0+1)/lenth
    return ascii_char[int(gray/unit)]

if __name__ =='__main__':
    customers = ['a','b','c']
    customers[2:4] = ['d','e','f']
    print('C:\some\name')
    im = Image.open('timg.jpg')
    im = im.resize((80,80),Image.NEAREST)

    txt = ""

    for i in range(80):
        for j in range(80):
            txt += get_char(*im.getpixel((j,i)))
        txt += '\n'

    print(txt)
    with open('output.txt','w') as f:
        f.write(txt)
