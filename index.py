from Classes.NewsLoaderMirror import NewsLoaderMirror
from Classes.TokenService import TokenService

def main():
    # mirrorLoader = NewsLoaderMirror('mirror', 5)
    # print(mirrorLoader.getNewsMappers())
    tokenService = TokenService()
    print(tokenService.getToken())

if __name__ == '__main__':
    main()
