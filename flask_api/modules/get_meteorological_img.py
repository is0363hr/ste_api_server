# 気象庁画像取得（2021/3/11）
from flask.app import Flask
import requests
from datetime import datetime, timedelta
import os
import cv2
import base64
import time
import os

from modules.line_api import LinePush
from config.map_param import ZOOM_SCOP
from modules.db_controller import DBFunc


def image_file_to_base64(file_path):
    with open(file_path, "rb") as image_file:
        data = base64.b64encode(image_file.read())
    return data.decode('utf-8')


class MeteImg:
    def __init__(self) -> None:
        self.tag = None # map or cloud
        self.on_time = None
        self.forecast_time = None
        self.zoom = None
        self.x = None
        self.y = None
        self.db_func = DBFunc()


    # 2021/04/01/13/57/00 -> 20210401045500
    def convert_time(self, date_data):
        h = sum([int(s) for s in str(date_data.strftime("%H"))])
        m = int(date_data.strftime("%M")[-1])
        temp_time = date_data - timedelta(minutes=5 + m % 5)
        time = list(temp_time.strftime("%Y%m%d%H%M"))
        if h < 10:
            time[-4:-2] = "0" + str(h)
        else:
            time[-4:-2] = str(h)
        time = "".join(time) + '00'
        return time


    def create_cloud_img_url(self):
        on_time = self.convert_time(self.on_time)
        forecast_time = self.convert_time(self.forecast_time)
        cloud_img_url = CLOUD_IMAGE_BASE_URL + "{}/none/{}/surf/hrpns/{}/{}/{}.png".format(on_time, forecast_time, self.zoom, self.x, self.y)
        return cloud_img_url


    def create_map_img_url(self):
        map_img_url = MAP_IMAGE_URL + "{}/{}/{}.png".format(self.zoom, self.x, self.y)
        return map_img_url


    def create_save_img_path(self):
        if self.tag == 'map':
            output_path = SAVE_BASE_DIR + "{}/{}/{}_{}.png".format(self.tag, self.zoom, self.x, self.y)
        elif self.tag == 'cloud':
            output_path = SAVE_BASE_DIR + "{}/{}/{}/{}_{}-{}_{}.png".format(self.tag, self.zoom, str(self.on_time.strftime("%Y_%m_%d")), self.convert_time(self.on_time)[-6:], self.convert_time(self.forecast_time)[-6:], self.x, self.y)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        return output_path


    def get_img(self):
        if self.tag == 'map':
            url = self.create_map_img_url()
        elif self.tag == 'cloud':
            url = self.create_cloud_img_url()

        output_path = self.create_save_img_path()
        # print(os.path.basename(output_path))
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
        return output_path


    def bulk_get_img(self, tag, on_time, forecast_time):
        self.tag = tag
        self.on_time = on_time
        self.forecast_time = forecast_time
        data_list = []
        for zoom_temp in ZOOM_SCOP:
            for x in range(zoom_temp['X_INITIALIZE_MIN'], zoom_temp['X_INITIALIZE_MAX']+1):
                for y in range(zoom_temp['Y_INITIALIZE_MIN'], zoom_temp['Y_INITIALIZE_MAX']+1):
                    self.zoom = zoom_temp['ZOOM']
                    self.x = x
                    self.y = y
                    img_path = self.get_img()
                    data_list.append({
                        'img_path': img_path,
                        'img_time': forecast_time,
                        'created_at': on_time,
                        'tag': tag,
                        'zoom_level': self.zoom,
                    })
                    time.sleep(1)
        self.db_func.bulk_insert_data(data_list)
        return


# const ----------------
SAVE_BASE_DIR = './static/'
MAP_IMAGE_URL = "https://cyberjapandata.gsi.go.jp/xyz/pale/"
CLOUD_IMAGE_BASE_URL = "https://www.jma.go.jp/bosai/jmatile/data/nowc/"
# ----------------------


def main():
    now = datetime.now()
    print(now)
    mimg = MeteImg()
    mimg.bulk_get_img('cloud', now, now)
    pass


if __name__ == "__main__":
    main()