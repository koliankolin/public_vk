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

    def loadMem(self):
        ua = UserAgent()
        headers = {
            'User-Agent': ua.chrome
        }
        img_data = requests.get(self.photo_link, headers=headers).content
        file_name = f'./img/sample.png'
        with open(file_name, 'wb') as handler:
            handler.write(img_data)

        file_mem = self._createMemFromPhoto(file_name)
        # return file_mem
        photo = self.uploader.photo_wall(file_mem, group_id=constants.VK_GROUP_ID)[0]
        return 'photo{owner_id}_{id}'.format(**photo)

    def loadPhoto(self, file_path):
        photo = self.uploader.photo_wall(file_path, group_id=constants.VK_GROUP_ID)[0]
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

    def createRatingPhoto(self, leaderBoards, date, path_file='img/leader_board.png'):
        width, height = 800, 900
        thumb = 64, 64

        img = Image.new('RGBA', (width, height), color='white')
        fnt = ImageFont.truetype('fonts/YesevaOne-Regular.ttf', int(img.size[0] * 0.04))
        fnt_point = ImageFont.truetype('fonts/Roboto-Regular.ttf', int(img.size[0] * 0.04))

        d = ImageDraw.Draw(img)

        header = 'Топчики Недели'
        w, h = d.textsize(header, font=fnt)
        txt_height = img.size[1] * 0.01
        d.text(((img.size[0] - w) / 2, txt_height), header, font=fnt, fill='black')

        w, h = d.textsize(date, font=fnt)
        d.text(((img.size[0] - w) / 2, h + 10), date, font=fnt, fill='black')

        # d.text((15, img.size[1] * 0.8), '*Подробности в палике МамкиН КомментеР', font=fnt, fill='white')
        first_place = Image.open('img/icons/1st_place.png')
        first_place = first_place.convert("RGBA")
        first_place.thumbnail(thumb, Image.ANTIALIAS)

        second_place = Image.open('img/icons/2st_place.png')
        second_place = second_place.convert("RGBA")
        second_place.thumbnail(thumb, Image.ANTIALIAS)

        third_place = Image.open('img/icons/3rd_place.png')
        third_place = third_place.convert("RGBA")
        third_place.thumbnail(thumb, Image.ANTIALIAS)

        margin_top = int(img.size[0] * 0.08)

        lb = leaderBoards['best_comments']
        d.text((230, margin_top + 70 * 0.4), 'Рейтинг Комментов:', font=fnt, fill='black')
        img.alpha_composite(first_place, (10, margin_top + 70))
        d.text((70, margin_top + 80), f'{lb[0]["from_id"]} - {lb[0]["likes_count"]} likes', font=fnt_point, fill='black')
        img.alpha_composite(second_place, (10, margin_top + 70 * 2))
        d.text((70, margin_top + 70 * 2 + 10), f'{lb[0]["from_id"]} - {lb[0]["likes_count"]} likes', font=fnt_point, fill='black')
        img.alpha_composite(third_place, (10, margin_top + 70 * 3))
        d.text((70, margin_top + 70 * 3 + 10), f'{lb[0]["from_id"]} - {lb[0]["likes_count"]} likes', font=fnt_point, fill='black')

        lb = leaderBoards['comment']
        d.text((230, margin_top + 70 * 4.4), 'Рейтинг Комментеров:', font=fnt, fill='black')
        img.alpha_composite(first_place, (10, margin_top + 70 * 5))
        d.text((70, margin_top + 70 * 5 + 10), f'{list(lb.keys())[0]} - {list(lb.values())[0]} likes', font=fnt_point, fill='black')
        img.alpha_composite(second_place, (10, margin_top + 70 * 6))
        d.text((70, margin_top + 70 * 6 + 10), f'{list(lb.keys())[0]} - {list(lb.values())[0]} likes', font=fnt_point, fill='black')
        img.alpha_composite(third_place, (10, margin_top + 70 * 7))
        d.text((70, margin_top + 70 * 7 + 10), f'{list(lb.keys())[0]} - {list(lb.values())[0]} likes', font=fnt_point, fill='black')

        lb = leaderBoards['active']
        d.text((230, margin_top + 70 * 8.4), 'Рейтинг Активных:', font=fnt, fill='black')
        img.alpha_composite(first_place, (10, margin_top + 70 * 9))
        d.text((70, margin_top + 70 * 9 + 10), f'{list(lb.keys())[0]} - {list(lb.values())[0]} points', font=fnt_point, fill='black')
        img.alpha_composite(second_place, (10, margin_top + 70 * 10))
        d.text((70, margin_top + 70 * 10 + 10), f'{list(lb.keys())[0]} - {list(lb.values())[0]} points', font=fnt_point, fill='black')
        img.alpha_composite(third_place, (10, margin_top + 70 * 11))
        d.text((70, margin_top + 70 * 11 + 10), f'{list(lb.keys())[0]} - {list(lb.values())[0]} points', font=fnt_point, fill='black')

        img.save(path_file, 'PNG')

        return path_file