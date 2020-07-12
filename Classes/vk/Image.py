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
from datetime import date, timedelta

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
    def _createMemFromPhoto(photo_path, gradient=3., initial_opacity=1., path_out='./img/out.png'):
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

    def createRatingPhoto(self, leaderBoards):
        path_file = 'layouts/rating/rating_week_edit.png' if self.utils.checkIsSunday() else 'layouts/rating/rating_layout_edit.png'
        file_open = 'layouts/rating/rating_week.png' if self.utils.checkIsSunday() else 'layouts/rating/rating_layout.png'

        img = Image.open(file_open)
        img = img.convert("RGBA")

        fnt = ImageFont.truetype('fonts/Agency_Gothic.otf', 80)
        fnt_name = ImageFont.truetype('fonts/Agency_Gothic.otf', 70)

        week_day = date.today().weekday() + 1

        cover_phrase = f'{week_day} день {self.utils.getWeekId()} неделя' if not self.utils.checkIsSunday() else f'{self.utils.getWeekId()} неделя'

        d = ImageDraw.Draw(img)
        w, h = d.textsize(cover_phrase, font=fnt)
        d.text(((img.size[0] - w) / 2, 145), cover_phrase, font=fnt, fill='white')

        names, _ = self._getNamesAndPhotosFromLeaderBoard(leaderBoards, is_test=False)

        for name, height in zip(names, range(350, 800, 175)):
            w, h = d.textsize(name, font=fnt_name)
            d.text(((img.size[0] - w) / 2, height), name, font=fnt_name, fill='#1fb6b6')

        img.save(path_file)

        return path_file

    @staticmethod
    def _crop_center(pil_img, crop_width, crop_height):
        img_width, img_height = pil_img.size
        return pil_img.crop(((img_width - crop_width) // 2,
                             (img_height - crop_height) // 2,
                             (img_width + crop_width) // 2,
                             (img_height + crop_height) // 2))

    @staticmethod
    def _mask_circle_transparent(pil_img, blur_radius, offset=0):
        offset = blur_radius * 2 + offset
        mask = Image.new("L", pil_img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((offset, offset, pil_img.size[0] - offset, pil_img.size[1] - offset), fill=255)
        mask = mask.filter(ImageFilter.GaussianBlur(blur_radius))

        result = pil_img.copy()
        result.putalpha(mask)

        return result

    def _getNamesAndPhotosFromLeaderBoard(self, leaderBoards, is_test):
        if not is_test:
            ids = [
                leaderBoards['best_comments'][0]['from_id'],
                list(leaderBoards['comment'].keys())[0],
                list(leaderBoards['active'].keys())[0],
            ]

            names = [self.utils.getFullNameById([id_])[0] for id_ in ids]
            photos = [self.utils.downloadPhotoById(id_) for id_ in ids]
        else:
            names = ['Твое имя', 'Не твое имя', 'Имя твоего кота']
            photos = ['img/fills/fill.png', 'img/fills/fill.png', 'img/fills/fill.png']

        return names, photos

    def _getDaysLeft(self):
        return self.utils.plural_days(-(date.today() - constants.START_DATE).days).upper()

    def _createThumbsFromPhotos(self, photos, thumb_width=180):
        paste_imgs = [Image.open(photo) for photo in photos]
        im_thumbs = [self._crop_center(paste_img, thumb_width, thumb_width) for paste_img in paste_imgs]

        return [self._mask_circle_transparent(im_thumb, 3) for im_thumb in im_thumbs]

    def createCover(self, leaderBoards, is_test):
        path_file = 'layouts/cover_web_edit.png'
        file_open = 'layouts/cover_web_1.png'

        img = Image.open(file_open)
        img = img.convert("RGBA")
        thumb_width = 180

        cover_phrase = f'До старта уже {self._getDaysLeft()}' \
            if is_test else \
            f'Сейчас идет {self.utils.getWeekId()} неделя'

        fnt = ImageFont.truetype('fonts/Roboto-Regular.ttf', 25)
        fnt_days = ImageFont.truetype('fonts/Roboto-Regular.ttf', 40)

        names, photos = self._getNamesAndPhotosFromLeaderBoard(leaderBoards, is_test)
        im_thumbs = self._createThumbsFromPhotos(photos, thumb_width)

        d = ImageDraw.Draw(img)

        d.text((260, 310), cover_phrase, font=fnt_days, fill='white')

        img.alpha_composite(im_thumbs[0], (730, 40))
        d.text((730, 227), names[0], font=fnt, fill='white')

        img.alpha_composite(im_thumbs[1], (955, 40))
        d.text((970, 227), names[1], font=fnt, fill='white')

        img.alpha_composite(im_thumbs[2], (1175, 40))
        d.text((1180, 227), names[2], font=fnt, fill='white')

        img.save(path_file)

        return path_file

    def _createMobileCoverDay(self, leaderBoards, is_test):
        path_file = 'layouts/mobile/cover_mob_1_edit.png'
        file_open = 'layouts/mobile/cover_mob_1.png'

        img = Image.open(file_open)
        img = img.convert("RGBA")
        thumb_width = 230

        fnt = ImageFont.truetype('fonts/Roboto-Regular.ttf', 40)
        names, photos = self._getNamesAndPhotosFromLeaderBoard(leaderBoards, is_test)
        im_thumbs = self._createThumbsFromPhotos(photos, thumb_width)

        d = ImageDraw.Draw(img)

        img.alpha_composite(im_thumbs[0], (130, 670))
        d.text((100, 905), names[0], font=fnt, fill='white')

        img.alpha_composite(im_thumbs[1], (750, 670))
        d.text((750, 905), names[1], font=fnt, fill='white')

        img.alpha_composite(im_thumbs[2], (440, 1000))
        d.text((415, 1230), names[2], font=fnt, fill='white')

        img.save(path_file)

    def _createMobileCoverWeek(self, leaderBoards, is_test):
        path_file = 'layouts/mobile/cover_mob_2_edit.png'
        file_open = 'layouts/mobile/cover_mob_2.png'

        img = Image.open(file_open)
        img = img.convert("RGBA")
        thumb_width = 230

        fnt = ImageFont.truetype('fonts/Roboto-Regular.ttf', 40)

        if self.utils.checkIsSunday():
            self.utils.saveNamesAndPhotosWeek(*self._getNamesAndPhotosFromLeaderBoard(leaderBoards, is_test))
        names, photos = self.utils.getWeekNamesRating()

        im_thumbs = self._createThumbsFromPhotos(photos, thumb_width)

        d = ImageDraw.Draw(img)

        img.alpha_composite(im_thumbs[0], (130, 670))
        d.text((100, 905), names[0], font=fnt, fill='white')

        img.alpha_composite(im_thumbs[1], (750, 670))
        d.text((750, 905), names[1], font=fnt, fill='white')

        img.alpha_composite(im_thumbs[2], (440, 1000))
        d.text((415, 1230), names[2], font=fnt, fill='white')

        img.save(path_file)

    def _createMobileMainCover(self, is_test):
        path_file = 'layouts/mobile/layout_mob_edit.png'
        file_open = 'layouts/mobile/layout_mob.png'

        img = Image.open(file_open)
        img = img.convert("RGBA")

        fnt = ImageFont.truetype('fonts/Roboto-Regular.ttf', 80)
        cover_phrase = f'До старта уже {self._getDaysLeft()}' \
            if is_test else \
            f'Сейчас идет {self.utils.getWeekId()} неделя'

        d = ImageDraw.Draw(img)
        d.text((102, 1125), cover_phrase, font=fnt, fill='white')

        img.save(path_file)

    def createMobileCovers(self, leaderBoards, is_test):
        self._createMobileMainCover(is_test)
        self._createMobileCoverDay(leaderBoards, is_test)
        self._createMobileCoverWeek(leaderBoards, is_test)
