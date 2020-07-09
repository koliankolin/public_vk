import constants
from Classes.vk.Base import Base
from fake_useragent import UserAgent
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import textwrap
import requests
import math
import mem_const
import random
from Classes.image.Unsplash import Unsplash
from Classes.vk.Utils import Utils
from pprint import pprint

class ImageCls(Base):
    def __init__(self):
        super().__init__()
        self.photo_link = Unsplash().loadImageUrl()
        self.utils = Utils()

    def loadMem(self):
        # ua = UserAgent()
        # headers = {
        #     'User-Agent': ua.chrome
        # }
        # img_data = requests.get(self.photo_link, headers=headers).content
        # file_name = f'./img/sample.png'
        # with open(file_name, 'wb') as handler:
        #     handler.write(img_data)

        file_mem = self._createMemFromPhoto(self.utils.downloadPhotoByUrl(self.photo_link, './img/sample.png'))
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
        ids = [l_['from_id'] for l_ in lb]
        names = self.utils.getFullNameById(ids)
        values = [l_["likes_count"] for l_ in lb]
        if len(names) > 0:
            d.text((230, margin_top + 70 * 0.4), 'Рейтинг Комментов:', font=fnt, fill='black')
            img.alpha_composite(first_place, (10, margin_top + 70))
            d.text((70, margin_top + 80), f'{names[0]} - {values[0]} likes', font=fnt_point, fill='black')
        if len(names) > 1:
            img.alpha_composite(second_place, (10, margin_top + 70 * 2))
            d.text((70, margin_top + 70 * 2 + 10), f'{names[1]} - {values[1]} likes', font=fnt_point, fill='black')
        if len(names) > 2:
            img.alpha_composite(third_place, (10, margin_top + 70 * 3))
            d.text((70, margin_top + 70 * 3 + 10), f'{names[2]} - {values[2]} likes', font=fnt_point, fill='black')

        lb = leaderBoards['comment']
        names = self.utils.getFullNameById(list(lb.keys()))
        values = list(lb.values())
        if len(names) > 0:
            d.text((230, margin_top + 70 * 4.4), 'Рейтинг Комментеров:', font=fnt, fill='black')
            img.alpha_composite(first_place, (10, margin_top + 70 * 5))
            d.text((70, margin_top + 70 * 5 + 10), f'{names[0]} - {values[0]} likes', font=fnt_point, fill='black')
        if len(names) > 1:
            img.alpha_composite(second_place, (10, margin_top + 70 * 6))
            d.text((70, margin_top + 70 * 6 + 10), f'{names[1]} - {values[1]} likes', font=fnt_point, fill='black')
        if len(names) > 2:
            img.alpha_composite(third_place, (10, margin_top + 70 * 7))
            d.text((70, margin_top + 70 * 7 + 10), f'{names[2]} - {values[2]} likes', font=fnt_point, fill='black')

        lb = leaderBoards['active']
        names = self.utils.getFullNameById(list(lb.keys()))
        values = list(lb.values())
        if len(names) > 0:
            d.text((230, margin_top + 70 * 8.4), 'Рейтинг Активных:', font=fnt, fill='black')
            img.alpha_composite(first_place, (10, margin_top + 70 * 9))
            d.text((70, margin_top + 70 * 9 + 10), f'{names[0]} - {values[0]} points', font=fnt_point, fill='black')
        if len(names) > 1:
            img.alpha_composite(second_place, (10, margin_top + 70 * 10))
            d.text((70, margin_top + 70 * 10 + 10), f'{names[1]} - {values[1]} points', font=fnt_point, fill='black')
        if len(names) > 2:
            img.alpha_composite(third_place, (10, margin_top + 70 * 11))
            d.text((70, margin_top + 70 * 11 + 10), f'{names[2]} - {values[2]} points', font=fnt_point, fill='black')

        img.save(path_file, 'PNG')

        return path_file

    def createCover(self, leaderBoards):
        path_file = 'layouts/cover_web_edit.png'
        file_open = 'layouts/cover_web.png'

        img = Image.open(file_open)
        img = img.convert("RGBA")
        thumb_width = 180

        fnt = ImageFont.truetype('fonts/Roboto-Regular.ttf', 30)

        ids = [
            leaderBoards['best_comments'][0]['from_id'],
            list(leaderBoards['comment'].keys())[0],
            list(leaderBoards['active'].keys())[0],
        ]

        names = [self.utils.getFullNameById([id_])[0] for id_ in ids]
        photos = [self.utils.downloadPhotoById(id_) for id_ in ids]

        paste_imgs = [Image.open(photo) for photo in photos]

        def crop_center(pil_img, crop_width, crop_height):
            img_width, img_height = pil_img.size
            return pil_img.crop(((img_width - crop_width) // 2,
                                 (img_height - crop_height) // 2,
                                 (img_width + crop_width) // 2,
                                 (img_height + crop_height) // 2))

        im_thumbs = [crop_center(paste_img, thumb_width, thumb_width) for paste_img in paste_imgs]

        def mask_circle_transparent(pil_img, blur_radius, offset=0):
            offset = blur_radius * 2 + offset
            mask = Image.new("L", pil_img.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((offset, offset, pil_img.size[0] - offset, pil_img.size[1] - offset), fill=255)
            mask = mask.filter(ImageFilter.GaussianBlur(blur_radius))

            result = pil_img.copy()
            result.putalpha(mask)

            return result

        # im_square = im_thumb.resize((thumb_width, thumb_width), Image.LANCZOS)
        im_thumbs = [mask_circle_transparent(im_thumb, 3) for im_thumb in im_thumbs]

        d = ImageDraw.Draw(img)

        img.alpha_composite(im_thumbs[0], (750, 40))
        d.text((730, 260), '\n'.join(names[0].split(' ')), font=fnt, fill='white')

        img.alpha_composite(im_thumbs[1], (970, 40))
        d.text((990, 260), '\n'.join(names[1].split(' ')), font=fnt, fill='white')

        img.alpha_composite(im_thumbs[2], (1190, 40))
        d.text((1200, 260), '\n'.join(names[2].split(' ')), font=fnt, fill='white')

        img.save(path_file)

        return path_file
