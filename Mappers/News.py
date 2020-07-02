class News:
    def __init__(self, teaser_en, text_en, teaser_ru, text_ru, link, img, source):
        self.teaser_en = teaser_en
        self.text_en = text_en
        self.text_ru = text_ru
        self.teaser_ru = teaser_ru
        self.link = link
        self.img = img
        self.source = source

    def __str__(self):
        return f'en: {self.teaser_en}, ru: {self.teaser_ru}'

    def __repr__(self):
        return f'en: {self.teaser_en}, ru: {self.teaser_ru}'

