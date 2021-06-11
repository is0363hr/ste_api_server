from modules.line_api import LinePush


def main():
    line_push = LinePush()
    line_push.push_scraping_today()


if __name__ == "__main__":
    main()