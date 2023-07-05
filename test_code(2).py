import os
import sqlite3 as sql3
import sys
import math

import folium
from folium.map import FitBounds
from folium import Marker
from folium.plugins import MarkerCluster

import pandas as pd
from PyQt5 import uic
from PyQt5.QtCore import QUrl, QDir
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout


def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# 메인화면
main = resource_path('./qt/map_widget.ui')
main_class = uic.loadUiType(main)[0]

class MapWidget(QWidget, main_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.con = sql3.connect("../Git_project/database/jeju.db")
        self.cur = self.con.cursor()

        df = pd.read_csv('../Git_project/data_file/town_attraction.csv', usecols=['읍면동명', '관광지명', '위도', '경도'])
        df.columns = ['town', 'spot_name', 'latitude', 'longitude']

        # Folium 지도 생성
        self.map = folium.Map(location=[df.latitude.mean(), df.longitude.mean()], tiles='openstreetmap', zoom_start=10, control_scale=True)

        # 밀집 마커 표현: MarkerCluster()
        cluster = MarkerCluster()

        # 지도에 마커 추가_1
        for i, row in df.iterrows():
            iframe = f"{df.spot_name[i]}" + "<br/>" + f"위도 {df.latitude[i]}" + "<br/>" + f"경도 {df.longitude[i]}"
            popup = folium.Popup(iframe, min_width=100, max_width=100)
            # folium.Marker(location=[row['latitude'], row['longitude']], popup=popup,
            #               icon=folium.Icon(color='green', icon='star')).add_to(map)
            cluster.add_child(Marker(location=[row['latitude'], row['longitude']], popup=popup,
                                     icon=folium.Icon(color=self.color_select(row), icon='star')))
            self.map.add_child(cluster)

        # 지도에 마커 추가_2(위도, 경도의 중간 값)
        marker = folium.Marker(location=[df.latitude.mean(), df.longitude.mean()], zoom_start=15,
                               popup='<b>where is it now</b>').add_to(self.map)
        marker.add_child(folium.Popup("제주도 위경도 중심"))

        #지도 내 위경도 실시간표기
        formatter = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
        from folium import plugins
        plugins.MousePosition(
            position="topright",
            separator=" | ",
            empty_string="NaN",
            lng_first=True,
            num_digits=20,
            prefix="Coordinates:",
            lat_formatter=formatter,
            lng_formatter=formatter,
        ).add_to(self.map)

        # Folium 지도를 HTML로 변환
        self.map.save('Jeju.html')

        # Qt 위젯을 생성하고, HTML 파일을 로드
        self.webview = QWebEngineView()
        self.webview.load(QUrl.fromLocalFile(QDir.current().filePath('Jeju.html')))

        # 레이아웃 설정
        layout = QVBoxLayout()
        layout.addWidget(self.webview)
        self.setLayout(layout)

        self.color_select(row=df.town)

        self.focusing_by_chosen_list((33.3708091, 126.6935196))

    # 동/면리 구분에 따른 지도 출력 (콤보박스가 변할 때 마다 실행)
    # def show_fir_division_map(self, **kwargs):
    #     {'city' : [(),(),()..]} or {'town':[(),(),()..]}

    #dateframe


    # 업소 구분별로 색상/마커표기
    def color_select(self, row):
        print(f"0 : {row[0]}")  #남원읍
        print(f"1 : {row[1]}")  #금호제주리조트 아쿠아나
        if row[0] == '남원읍':
            return 'darkviolet'
        elif row[0] == '구좌읍':
            return 'dodgerblue'
        elif row[0] == '성산읍':
            return 'yellow'
        else:
            return 'green'

    #찜 목록 내의 위/경도만 지도에 마커로 표기한다.(음식점)


    # 하단의 리스트에서 선택한 마커가 지도의 중앙에 포커싱 될 수 있는 함수 원함
    # args: 리스트 선택 시 해당 장소의 위/경도가 tuple 형태로 넘어옴
    # 문제: 기존 html이 아닌
    def focusing_by_chosen_list(self, *args):
        latitude = args[0][0]
        longitude = args[0][1]
        bounds = [[math.floor(latitude),math.floor(longitude)], [math.ceil(latitude),round(longitude)]]
        print(bounds)
        map = folium.Map()
        marker = folium.Marker([latitude, longitude])
        map.add_child(marker)
        bounds = marker.get_bounds()
        map.fit_bounds(bounds)
        box = map.add_child(FitBounds(bounds))
        map.show_in_browser()

        # bounds = map.fit_bounds(marker.get_bounds())
        # map.add_child(FitBounds(bounds, padding_top_left=None,
        #                         padding_bottom_right=None,
        #                         padding=None,
        #                         max_zoom=None))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MapWidget()
    widget.show()
    sys.exit(app.exec_())
