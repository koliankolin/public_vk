import constants
from Classes.vk.Base import Base
from fake_useragent import UserAgent
from PIL import Image, ImageDraw, ImageFont
import textwrap
import requests
import math
import mem_const
import random
from Classes.image.Unsplash import Unsplash

class ImageCls(Base):
    def __init__(self):
        super().__init__()
        self.photo_link = Unsplash().loadImageUrl()

    def loadPhoto(self):
        ua = UserAgent()
        headers = {
            'User-Agent': ua.chrome
        }
        img_data = requests.get(self.photo_link, headers=headers).content
        file_name = f'./img/sample.png'
        with open(file_name, 'wb') as handler:
            handler.write(img_data)

        file_mem = self._createMemFromPhoto(file_name)
        return file_mem
        photo = self.uploader.photo_wall(file_mem, group_id=constants.VK_GROUP_ID)[0]
        return 'photo{owner_id}_{id}'.format(**photo)

    @staticmethod
    def _createMemFromPhoto(photo_path, gradient=1., initial_opacity=1., path_out='./img/out.png'):
        img = Image.open(photo_path)
        input_im = img.convert("RGBA")

        if input_im.mode != 'RGBA':
            input_im = input_im.convert('RGBA')
        width, height = input_im.size

        alpha_gradient = Image.new('L', (1, height), color=0xFF)
        for x, x1 in zip(range(height)[::-1], range(height)):
            a = int((initial_opacity * 255.) * (1. - gradient * float(x) / height))
            if a > 0:
                alpha_gradient.putpixel((0, x1), a)
            else:
                alpha_gradient.putpixel((0, x1), 0)
        #         print('{}, {:.2f}, {}'.format(x, float(x) / height, a))
        alpha = alpha_gradient.resize(input_im.size)

        black_im = Image.new('RGBA', (width, height), color=mem_const.GRADIENT_COLOR)  # i.e. black
        black_im.putalpha(alpha)

        # make composite with original image
        output_im = Image.alpha_composite(input_im, black_im)

        overlay = Image.new('RGBA', (img.size[0], img.size[1] + 150), mem_const.GRADIENT_COLOR)
        overlay.paste(output_im, (0, 0))

        img = overlay

        fnt = ImageFont.truetype(mem_const.FONT_MAIN, int(img.size[0] * 0.06))
        fnt_mir = ImageFont.truetype(mem_const.FONT_LINE, int(img.size[0] * 0.04))
        fnt_info = ImageFont.truetype(mem_const.FONT_MAIN, int(img.size[0] * 0.02))

        text = random.choice(mem_const.MEM_TEXTS)
        br = len(text) / 2
        wd = int(math.ceil(br / 10.0)) * 10
        para = textwrap.wrap(text, width=wd)

        current_h, pad = img.size[1] - img.size[1] * 0.23, 3

        d = ImageDraw.Draw(img)
        for line in para:
            w, h = d.textsize(line, font=fnt)
            d.text(((img.size[0] - w) / 2, current_h), line, font=fnt, fill=mem_const.MAIN_COLOR)
            current_h += h + pad

        source = mem_const.SOURCE
        w, h = d.textsize(source, font=fnt_mir)
        txt_height = img.size[1] * 0.7
        d.text(((img.size[0] - w) / 2, txt_height), source, font=fnt_mir, fill=mem_const.LINE_COLOR)

        d.text((15, img.size[1] * 0.95), mem_const.INFO, font=fnt_info, fill='white')

        top = (15, txt_height * 1.03)
        x = ((width - w) // 2) - 15
        left = (x, txt_height * 1.03)

        x1 = x + w + 30
        top1 = (x1, txt_height * 1.03)
        left1 = (width - 15, txt_height * 1.03)

        top2 = (15, img.size[1] - 10)
        left2 = (width - 15, img.size[1] - 10)

        d.line([top, left], fill=mem_const.LINE_COLOR, width=3)
        d.line([top1, left1], fill=mem_const.LINE_COLOR, width=3)
        d.line([top2, left2], fill=mem_const.LINE_COLOR, width=3)

        img.save(path_out, 'PNG')

        return path_out