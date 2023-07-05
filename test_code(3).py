from PyQt5 import uic
from PyQt5.QtCore import QUrl
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout

import sys
import os
import pandas as pd

import folium
from folium import plugins, FeatureGroup, Marker

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# 메인화면
main = resource_path('../qt/map_widget.ui')
main_class = uic.loadUiType(main)[0]

class DataSort:
    attraction_df = pd.read_csv('../data_file/town_attraction.csv', usecols=['읍면동명', '관광지명', '위도', '경도'])
    attraction_df.columns = ['town', 'attraction_name', 'latitude', 'longitude']

    lodging_df = pd.read_csv('../data_file/town_lodging.csv', usecols=['읍면동명', '숙박업소명', '위도', '경도'])
    lodging_df.columns = ['town', 'lodging_name', 'latitude', 'longitude']

class MapWidget(QWidget, main_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.resize(952, 775)

        self.webview = QtWebEngineWidgets.QWebEngineView(self.map_frame)
        self.map_frame.show()

        # 레이아웃 설정
        layout = QVBoxLayout()
        layout.addWidget(self.webview)
        self.setLayout(layout)

        # ==============함수 호출============
        # 특정 위/경도에 해당하는 마커표기 및 지도 출력
        # self.focus_map('바닷가', [33.27264281, 126.7014326])

        # 첫번째 콤보박스 분류에 따른 마커 표기 및 지도 출력
        self.attraction_lodging_map()

        # 두번재 콤보박스 분류에 따른 마커 표기 및 지도 출력
        # self.attraction_or_lodging_map(DataSort.attraction_df, DataSort.lodging_df)

        # 애완동물 동반가능에 따른 마커 표기 및 지도 출력

    # 분류에 따른 html을 웹뷰객체에 설정
    def open_map(self, map):
        self.webview.setUrl(QUrl(f'file:///{map}'))
        self.webview.show()

    # 첫 콤보박스 (동/면/리) 함수
    # 현재 입력된 위경도는 제주도 관광명소지들의 중앙 위경도 값이다.
    def attraction_lodging_map(self):

        At_df = DataSort.attraction_df
        Lo_df = DataSort.lodging_df

        # 첫 콤보박스 값에 따라 관광/숙박 데이터프레임 변경
        At_df = At_df[At_df['town'] == '한림읍']
        Lo_df = Lo_df[Lo_df['town'] == '한림읍']

        # Folium 지도 생성
        map = folium.Map(location=[At_df.latitude.mean(), At_df.longitude.mean()],
                         tiles='openstreetmap', zoom_start=16, control_scale=True)

        # 지도 내 위경도 실시간 표기
        formatter = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
        plugins.MousePosition(
            position="topright",
            separator=" | ",
            empty_string="NaN",
            lng_first=True,
            num_digits=20,
            prefix="Coordinates:",
            lat_formatter=formatter,
            lng_formatter=formatter,
        ).add_to(map)

        # 근거리 마커 군집화
        cluster_1 = plugins.MarkerCluster()
        cluster_2 = plugins.MarkerCluster()

        # 마커 생성_1 (관광 중앙 위경도)
        marker = folium.Marker(location=[At_df.latitude.mean(), At_df.longitude.mean()],
                               zoom_start=15, icon=folium.Icon(icon='cloud')).add_to(map)
        marker.add_child(folium.Popup("제주도 위경도 중심", min_width=100, max_width=100))

        # 마커 생성_2 (관광)
        for i, row in At_df.iterrows():
            iframe = f"{At_df.attraction_name[i]}" + "<br/>" + f"위도 {At_df.latitude[i]}" + "<br/>" + f"경도 {At_df.longitude[i]}"
            popup = folium.Popup(iframe, min_width=100, max_width=100)
            cluster_1.add_child(Marker(location=[row['latitude'], row['longitude']], popup=popup,
                                       icon=folium.Icon(color='orange', icon='flag')))
            map.add_child(cluster_1)

        # 마커 생성_3 (숙박)
        for k, row in Lo_df.iterrows():
            iframe = f"{Lo_df.lodging_name[k]}" + "<br/>" + f"위도 {Lo_df.latitude[k]}" + "<br/>" + f"경도 {Lo_df.longitude[k]}"
            popup = folium.Popup(iframe, min_width=100, max_width=100)
            icon = plugins.BeautifyIcon(
                icon='star',text_color='#b3334f',
                background_color='transparent', border_color='transparent',
                inner_icon_style='font-size:20px')
            cluster_2.add_child(Marker(location=[row['latitude'], row['longitude']], popup=popup,
                                       icon=icon))
            map.add_child(cluster_2)

        # Folium 지도를 HTML로 변환
        map.save('map_1.html')
        show_map = 'map_1.html'
        self.open_map(show_map)

    def attraction_or_lodging_map(self, df_1, df_2):
        feature_group = FeatureGroup(name='관광명소/숙박업소')

        group_1 = plugins.FeatureGroupSubGroup(feature_group, '관광명소')
        group_2 = plugins.FeatureGroupSubGroup(feature_group, '숙박업소')

        map = folium.Map(location=[33.27264281, 126.7014326], zoom_start=15)

        for i, row in df_1.iterrows():
            map.add_child(feature_group)
            map.add_child(group_1)
            group_1.add_child(Marker(location=[row['latitude'], row['longitude']]))

        for k, row in df_2.iterrows():
            map.add_child(feature_group)
            map.add_child(group_2)
            group_2.add_child(Marker(location=[row['latitude'], row['longitude']]))

        layer_control = folium.LayerControl(collapsed=False)
        layer_control.add_to(map)
        folium.Element(
            '<style>.leaflet-control-layers-overlays span { '
            '  font-family: Arial;'
            '  color: green;'
            '}</style>'
        ).add_to(map.get_root().header)
        map.save('attraction.html')
        show_map = 'attraction.html'
        self.open_map(show_map)

    def focus_map(self, name, row):
        # print(row[0]) #위도
        # print(row[1]) #경도

        # location에 따라 마커 생성 및 포커싱
        show_map = folium.Map(location=[row[0], row[1]], zoom_start=18)
        marker = folium.Marker(location=[row[0], row[1]], icon=folium.Icon(icon='cloud')).add_to(show_map)
        marker.add_child(folium.Popup(f"{name}"+"<br/>"+"<a href=https://www.google.com/maps/@/data=!3m7!1e1!3m5!1sPrV4G2G7HtVEkhDoXE2eFw!2e0!6shttps:%2F%2Fstreetviewpixels-pa.googleapis.com%2Fv1%2Fthumbnail%3Fpanoid%3DPrV4G2G7HtVEkhDoXE2eFw%26cb_client%3Dsearch.revgeo_and_fetch.gps%26w%3D96%26h%3D64%26yaw%3D118.74289%26pitch%3D0%26thumbfov%3D100!7i13312!8i6656?entry=ttu</a>",
                                      min_width=100, max_width=100))

        #focus_map으로 지도 내 마커 갱신
        show_map.save('focus_map.html')
        # C = open('focus_map.html', 'r', encoding='utf-8')
        # html_ = C.read()
        self.webview.setUrl(QUrl('file:///focus_map.html'))
        self.webview.show()

    # def color_select(self, row):
    #     print(f"0 : {row[0]}")  #남원읍
    #     print(f"1 : {row[1]}")  #금호제주리조트 아쿠아나
    #     if row[0] == '남원읍':
    #         return 'red'
    #     elif row[0] == '구좌읍':
    #         return 'blue'
    #     elif row[0] == '성산읍':
    #         return 'yellow'
    #     else:
    #         return 'green'

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MapWidget()
    widget.show()
    app.exec()


