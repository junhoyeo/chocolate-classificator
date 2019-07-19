import os
from PIL import Image

def alpha_to_color(image):
    image = image.convert('RGBA')
    image.load()
    background = Image.new('RGB', image.size, (255, 255, 255))
    background.paste(image, mask=image.split()[3])
    return background

if __name__ == '__main__':
    for dir_name in ['dark_chocolate', 'white_chocolate']:
        dir_path = './downloads/{}'.format(dir_name)
        for image_path in os.listdir(dir_path):
            image_path = '{}/{}'.format(dir_path, image_path)

            if '.png' in image_path:
                png = Image.open(image_path)
                background = alpha_to_color(png)

                image_name = image_path.replace('png', 'jpg')
                background.save(image_name, 'JPEG', quality=80)
                os.remove(image_path)
                print('{} ===> {}'.format(image_path, image_name))

            with open(image_path, 'rb') as image_file:
                if bytes('<!DOCTYPE html>', 'UTF-8') in image_file.read():
                    print('[*] Found wrong image file: {}'.foramt(image_path))
                    os.remove(image_path)
