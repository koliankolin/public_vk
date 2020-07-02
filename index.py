from Classes.vk.ImageLoader import ImageLoader


def main():
    # mirrorLoader = NewsLoaderMirror('mirror', 5)
    # print(mirrorLoader.getNewsMappers())
    imgLoader = ImageLoader('code_email.png')
    print(imgLoader.loadPhoto())


if __name__ == '__main__':
    main()
