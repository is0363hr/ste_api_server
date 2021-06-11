# -*- coding: utf-8 -*-
from sqlalchemy.sql import func
from pprint import pprint
from datetime import datetime
from glob import glob
import os

from common.models.cloud import Cloud
from application import session


# const ----------------
# ./static/cloud/zoom/date/file
IMG_CLOUD_DIR = './static/cloud/*/*/*.png'
# ----------------------


class DBFunc:
    def __init__(self) -> None:
        pass

    # 最新の画像パスを取得
    def get_latest_img_path(self):
        max_id = session.query(func.max(Cloud.id)).scalar()
        cloud_img_path = (
            session.query(Cloud.img_path).filter(Cloud.id == max_id).scalar()
        )
        return cloud_img_path

    def get_latest_img_time(self):
        max_id = session.query(func.max(Cloud.id)).scalar()
        result = session.query(Cloud.img_time).filter(Cloud.id == max_id).scalar()
        cloud_img_time = result.strftime("%Y年%m月%d日%H時%M分")
        return cloud_img_time

    def get_all(self):
        # Userテーブルのnameカラムをすべて取得
        clouds = session.query(Cloud).all()
        data = []
        for cloud in clouds:
            data.append(
                {
                    "id": cloud.id,
                    "img_name": cloud.img_name,
                    "img_cloud_path": cloud.img_cloud_path,
                    "img_sye_path": cloud.img_sye_path,
                    "created_at": cloud.created_at,
                    "tag": cloud.tag,
                    "zoom_level": cloud.zoom_level,
                }
            )
        return data

    def get_all_img_cloud_path(self):
        data = self.get_all()
        img_path_list = [d['img_cloud_path'] for d in data]
        return img_path_list

    def get_today(self):
        now = datetime.date()
        clouds = session.query(Cloud).\
            filter(Cloud.created_at >= now).\
                all()

        return clouds

    def remove_id(self, id):
        try:
            cloud = session.query(Cloud).\
                filter(Cloud.id == id).\
                    all()

            session.delete(cloud)
            os.remove(cloud.img_cloud_path)
        except Exception as e:
            print("削除失敗")
        else:
            print("削除完了")
        return


    def remove_database_consistency(self, id):
        try:
            data = self.get_all_img_cloud_path()
            for file in glob(IMG_CLOUD_DIR):
                if file in data:
                    continue
                else:
                    os.remove(file)
        except Exception as e:
            print("削除失敗")
        else:
            print("削除完了")
        return


    def insert_data(self, img_path, img_time, created_at, tag, zoom_level):
        try:
            cloud = Cloud()
            cloud.img_name = os.path.basename(img_path)
            cloud.img_cloud_path = img_path
            # cloud.img_sye_path = ""
            cloud.img_time = os.path.splitext(os.path.basename(img_path))[0]
            cloud.created_at = created_at
            cloud.tag = tag
            cloud.zoom_level = zoom_level
            session.add(cloud)
            session.commit()
        except Exception as e:
            print("データベース追加失敗")
        else:
            log = "{}：{} 追加完了".format(created_at, os.path.basename(img_path))
            print(log)
        return

    def bulk_insert_data(self, data_list):
        now = datetime.now()
        cloud_list = []
        for d in data_list:
            cloud_list.append(
                Cloud(
                    img_name = os.path.basename(d['img_path']),
                    img_cloud_path = d['img_path'],
                    # img_sye_path = "",
                    img_time = d['img_time'],
                    created_at = d['created_at'],
                    tag = d['tag'],
                    zoom_level = d['zoom_level']
                )
            )
        try:
            session.add_all(cloud_list)
            session.commit()
        except Exception as e:
            log = "{}: データベース追加失敗".format(now)
            print(log)
            print(e)
        else:
            log = "{}：追加完了".format(now)
            print(log)
        return



def main():
    db = DBFunc()
    pprint(db.get_all())
    pass


if __name__ == "__main__":
    main()