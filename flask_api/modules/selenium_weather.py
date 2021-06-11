import chromedriver_binary # nopa
from selenium import webdriver


class Weather:
    def __init__(self) -> None:
        pass


    def get_weather(self):
        load_url = "https://www.jma.go.jp/bosai/#pattern=forecast&area_type=class20s&area_code=2520600"

        # WebDriver のオプションを設定する
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        driver.get(load_url)
        contents = str(driver.find_element_by_id("bosaitop-bosai_forecast_table_div").text)

        # ブラウザを終了する
        driver.quit()
        return contents


    def get_weather_tomorrow(self):
        content = self.get_weather()
        content_list = ''.join(content.split(' '))
        content_list = content_list.split('\n')
        i = 0
        flag = False
        weather = ''
        for con in content_list:
            if flag:
                i += 1
            if i == 2:
                weather = con
            if '南部' == con:
                flag = True

        return weather


def main():
    pass
    # return get_weather_tomorrow()


if __name__ == "__main__":
    main()