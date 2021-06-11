# 気象庁画像取得（2021/3/11）

import requests
from datetime import datetime, timedelta
import os
import cv2


class meteorogical_img:
    def __init__(
        self,
        tag,
        line_range_min,
        line_range_max,
        column_range_min,
        column_range_max,
        zoom,
    ) -> None:
        self.tag = tag
        self.line_range_min = line_range_min
        self.line_range_max = line_range_max
        self.column_range_min = column_range_min
        self.column_range_max = column_range_max
        self.zoom = zoom

        pass

    def get_map_img(self):
        now = datetime.now()
        h = sum([int(s) for s in str(now.strftime("%H"))])
        m = int(now.strftime("%M")[-1])
        temp_time = datetime.now() - timedelta(minutes=5 + m % 5)
        time = list(temp_time.strftime("%Y%m%d%H%M"))
        if h < 10:
            time[-4:-2] = "0" + str(h)
        else:
            time[-4:-2] = str(h)
        time = "".join(time)
        print(time)
        # time = "202101060955"
        # self.img_time = temp_time.strftime("%Y年%m月%d日%H時%M分")
        self.img_time = temp_time
        if self.tag == "map":
            base_url = "https://cyberjapandata.gsi.go.jp/xyz/pale/"
        elif self.tag == "cloud":
            base_url = "https://www.jma.go.jp/bosai/jmatile/data/nowc/20210225111500/none/20210225111500/surf/hrpns/"
        for column in range(self.column_range_min, self.column_range_max + 1):
            for line in range(self.line_range_min, self.line_range_max + 1):
                url = (base_url + "{}/{}/{}.png").format(
                    self.zoom,
                    column,
                    line,
                )
                output_path = ("./img/{}/{}/{}_{}.png").format(
                    self.tag, self.zoom, column, line
                )
                dir = os.path.dirname(output_path) + "/"
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                self.save_img(url, output_path)
        return dir

    # 指定したURLの画像を保存
    def save_img(self, url, output_path):
        try:
            req = requests.get(url)
            with open(output_path, "wb") as w:
                w.write(req.content)
                w.close()
        except requests.exceptions.HTTPError:
            print("{}へのアクセス失敗".format(url))
        except Exception as e:
            print(e)

    # 画像結合
    def img_connect(self, path):
        flag = False
        if self.tag == "cloud":
            flag = True
        v_list = []
        for i in range(self.column_range_min, self.column_range_max + 1):
            file = path + str(i) + "_" + str(self.line_range_min) + ".png"
            if flag:
                base_img = cv2.imread(file, -1)
            else:
                base_img = cv2.imread(file)
            for j in range(self.line_range_min + 1, self.line_range_max + 1):
                file = path + str(i) + "_" + str(j) + ".png"
                if flag:
                    im = cv2.imread(file, -1)
                else:
                    im = cv2.imread(file)
                base_img = cv2.vconcat([base_img, im])
            v_list.append(base_img)
        base_img = v_list[0]
        for v in v_list[1:]:
            base_img = cv2.hconcat([base_img, v])

        cv2.imwrite(path + "result.png", base_img)

    # 透過画像の合成
    def sye(self):
        cartopy = False
        base_path = "./img"
        if cartopy:
            map = "cartopy/"
        else:
            map = "map/"
        map_path = ("{}/{}/{}/result.png").format(base_path, "map", self.zoom)
        cloud_path = ("{}/{}/{}/result.png").format(base_path, "cloud", self.zoom)
        map = cv2.imread(map_path)
        # height, width = map.shape[0], map.shape[1]
        # map = cv2.resize(map, (512, 512))
        cloud = cv2.imread(cloud_path, -1)
        # 貼り付け先座標の設定。とりあえず左上に
        x1, y1, x2, y2 = 0, 0, cloud.shape[1], cloud.shape[0]

        map[y1:y2, x1:x2] = map[y1:y2, x1:x2] * (1 - cloud[:, :, 3:] / 255) + cloud[
            :, :, :3
        ] * (cloud[:, :, 3:] / 255)
        output_path = ("{}/{}/{}/result.png").format(base_path, "sye", self.zoom)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        cv2.imwrite(output_path, map)
        return output_path


def main():
    zoom = 5
    # /column_line/
    column_range_min = 27
    column_range_max = 29
    line_range_min = 11
    line_range_max = 14
    tag = "map"
    meteoro = meteorogical_img(
        tag, line_range_min, line_range_max, column_range_min, column_range_max, zoom
    )
    path = meteoro.get_map_img()
    meteoro.img_connect(path)
    meteoro.sye()


if __name__ == "__main__":
    main()

    pass