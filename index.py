from Classes.NewsLoaderMirror import NewsLoaderMirror


def main():
    mirrorLoader = NewsLoaderMirror('mirror', 5)
    print(mirrorLoader.getNewsMappers())


if __name__ == '__main__':
    main()
