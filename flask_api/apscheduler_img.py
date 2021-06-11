from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from io import BytesIO
from PIL import Image
import os

# 実行ディレクトリを上げる
# import sys
# sys.path.append("../")
# from modules.meteorological_img import meteoro_img_create
from modules.get_meteorological_img import MeteImg
from common.models.cloud import Cloud

# セッション変数の取得
from application import session


class Map_update:
    def __init__(self) -> None:
        self.scheduler = BackgroundScheduler(standalone=True, coalesce=True)
        pass

    def sche_second_set(self, set_time):
        self.scheduler.add_job(self.regular_insert_img, "interval", seconds=set_time)

    def sche_minute_set(self, set_time):
        self.scheduler.add_job(self.regular_insert_img, "interval", minutes=set_time)

    def sche_start(self):
        self.scheduler.start()

    def sche_shutdown(self):
        self.scheduler.shutdown()

    def sche_pause(self):
        self.scheduler.pause()

    def img_io(self, path):
        image_data = BytesIO()
        im = Image.open(path)
        im.save(image_data, "png")
        image_data.seek(0)
        image_file = image_data.read()
        return image_file

    # def regular_insert_img(self):
    #     now = datetime.now()
    #     zoom = 4
    #     cloud_path, sye_path = meteoro_img_create(now, 135, 34, zoom)
    #     cloud = Cloud()
    #     cloud.img_name = os.path.basename(cloud_path)
    #     cloud.img_cloud_path = cloud_path
    #     cloud.img_sye_path = sye_path
    #     cloud.img_time = os.path.splitext(os.path.basename(cloud_path))[0]
    #     cloud.created_at = now
    #     cloud.tag = "cloud"
    #     cloud.zoom_level = zoom
    #     session.add(cloud)
    #     session.commit()
    #     print(cloud_path)
    #     print("regular_insert")

    def regular_insert_img(self):
        now = datetime.now()
        mimg = MeteImg()
        mimg.bulk_get_img('cloud', now, now)
        

    def request_insert_img(self, request_datetime, zoom, path):
        cloud = Cloud()
        cloud.img_name = os.path.basename(path)
        cloud.img_path = path
        cloud.img_time = os.path.splitext(os.path.basename(path))[0]
        cloud.created_at = request_datetime
        cloud.tag = "synthetic"
        cloud.zoom_level = zoom
        session.add(cloud)
        session.commit()
        print(path)
        print("request_insert")


def main():
    print("schedule start")
    map = Map_update()
    map.sche_second_set(10)
    map.sche_start()


if __name__ == "__main__":
    main()
