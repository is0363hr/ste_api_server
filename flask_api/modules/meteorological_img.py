# 気象庁画像取得（2021/3/11）
from flask.app import Flask
from modules.line_api import LinePush
import requests
from datetime import datetime, timedelta
import os
import cv2
import base64


def strToDate(year, month, day, hour, minute):
    tstr = year + month + day + hour + minute
    tdate = datetime.strptime(tstr, '%Y%m%d%H%M')
    return tdate


def image_file_to_base64(file_path):
    with open(file_path, "rb") as image_file:
        data = base64.b64encode(image_file.read())
    return data.decode('utf-8')


class MeteImg:
    def __init__(
        self,
        dateTime,
        lon,
        lat,
        zoom,
    ) -> None:
        self.tag = ""
        self.dateTime = dateTime
        self.lon = lon
        self.lat = lat
        self.zoom = zoom
        self.column = 0
        self.line = 0
        self.get_time = ''



    def get_img(self, datetime_set=False):
        if not datetime_set:
            date_data = datetime.now()
        else:
            date_data = self.dateTime
        h = sum([int(s) for s in str(date_data.strftime("%H"))])
        m = int(date_data.strftime("%M")[-1])
        temp_time = date_data - timedelta(minutes=5 + m % 5)
        time = list(temp_time.strftime("%Y%m%d%H%M"))
        if h < 10:
            time[-4:-2] = "0" + str(h)
        else:
            time[-4:-2] = str(h)
        time = "".join(time) + '00'
        self.get_time = time
        # print(time)
        # time = "202101060955"
        # self.img_time = temp_time.strftime("%Y年%m月%d日%H時%M分")
        self.img_time = temp_time
        if self.tag == "map":
            base_url = "https://cyberjapandata.gsi.go.jp/xyz/pale/"
        elif self.tag == "cloud":
            base_url = ("https://www.jma.go.jp/bosai/jmatile/data/nowc/{}/none/{}/surf/hrpns/").format(time, time)

        z, x, y = self.get_column_line()

        for i in range(z):
            for j in range(z):
                url = (base_url + "{}/{}/{}.png").format(
                    self.zoom,
                    x+i,
                    y+j,
                )
                output_path = (SAVE_DIR+"/{}/{}/{}_{}.png").format(
                    self.tag, self.zoom, x+i, y+j
                )
                dir = os.path.dirname(output_path) + "/"+ str(date_data.strftime("%Y_%m_%d")) + "/"
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                self.save_img(url, output_path)
                print(url)
        return dir

    # 指定したURLの画像を保存
    def save_img(self, url, output_path):
        try:
            req = requests.get(url)
            with open(output_path, "wb") as w:
                w.write(req.content)
                w.close()
        except requests.exceptions.HTTPError as request_error:
            print("{}へのアクセス失敗".format(url))
            line_push = LinePush()
            line_push.push_scraping_error(request_error)
        except Exception as e:
            print("アクセス失敗!!!")
            line_push = LinePush()
            line_push.push_scraping_error(e)
            print(e)

    # 画像結合
    def img_connect(self, path):
        z, x, y = self.get_column_line()
        v_list = []
        for i in range(z):
            for j in range(z):
                file = path + str(x+i) + "_" + str(y+j) + ".png"
                if not (j==0):
                    if self.tag == "cloud":
                        im = cv2.imread(file, -1)
                    else:
                        im = cv2.imread(file)
                    base_img = cv2.vconcat([base_img, im])
                elif j==0:
                    if self.tag == "cloud":
                        base_img = cv2.imread(file, -1)
                    else:
                        base_img = cv2.imread(file)
            v_list.append(base_img)
        base_img = v_list[0]
        for v in v_list[1:]:
            base_img = cv2.hconcat([base_img, v])

        output_path = path + self.get_time + ".png"
        cv2.imwrite(output_path, base_img)
        return output_path

    # 透過画像の合成
    def sye(self, cloud_path):
        cartopy = False
        base_path = SAVE_DIR
        if cartopy:
            map = "cartopy/"
        else:
            map = "map/"
        map_path = ("{}/{}/{}/result.png").format(base_path, "map", self.zoom)
        # cloud_path = ("{}/{}/{}/{}.png").format(base_path, "cloud", self.zoom, self.get_time)
        map = cv2.imread(map_path)
        # height, width = map.shape[0], map.shape[1]
        # map = cv2.resize(map, (512, 512))
        cloud = cv2.imread(cloud_path, -1)
        # 貼り付け先座標の設定。とりあえず左上に
        x1, y1, x2, y2 = 0, 0, cloud.shape[1], cloud.shape[0]

        map[y1:y2, x1:x2] = map[y1:y2, x1:x2] * (1 - cloud[:, :, 3:] / 255) + cloud[
            :, :, :3
        ] * (cloud[:, :, 3:] / 255)
        output_path = ("{}/{}/{}/{}.png").format(base_path, "sye", self.zoom, self.get_time)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        cv2.imwrite(output_path, map)
        return output_path


    def get_column_line(self):
        self.line = LINE_INITIALIZE_NUMBER
        self.column = COLUMN_INITIALIZE_NUMBER
        zoom_range = self.zoom - ZOOM_INITIALIZE + 1
        return zoom_range+1, zoom_range*self.line, zoom_range*self.column


    def map_create(self):
        self.tag = "map"
        path = self.get_img()
        self.img_connect(path)
        return


    def cloud_create(self, datetime_set=False):
        self.tag = "cloud"
        path = self.get_img(datetime_set)
        cloud_path = self.img_connect(path)
        sye_path = self.sye(cloud_path)
        return cloud_path, sye_path


def meteoro_img_create(dateTime, lon, lat, zoom):
    meteoro = MeteImg(
        dateTime, lon, lat, zoom
    )
    meteoro.map_create()
    return meteoro.cloud_create()

# 日本地図の初期位置
ZOOM_INITIALIZE  = 4
LINE_INITIALIZE_NUMBER = 13
COLUMN_INITIALIZE_NUMBER = 5
SAVE_DIR = './static'


def main():
    zoom = 4
    now = datetime.now()
    now = strToDate(
        '2021',
        '4',
        '10',
        '22',
        '35'
    )
    mimg = MeteImg(
        now,
        '34',
        '135',
        4,
    )
    print(mimg.cloud_create(True))


if __name__ == "__main__":
    main()
