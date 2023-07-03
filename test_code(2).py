import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
import folium
from folium.plugins import FastMarkerCluster

Qt 애플리케이션을 정의하고, 지도를 보여줄 위젯을 생성하세요.

python
Copy code
class MapWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Folium 지도 생성
        m = folium.Map(location=[37.5665, 126.9780], zoom_start=12)

        # 지도에 마커 추가
        folium.Marker(location=[37.5665, 126.9780], popup="Seoul").add_to(m)

        # Folium 지도를 HTML로 변환
        m.save('map.html')

        # Qt 위젯을 생성하고, HTML 파일을 로드
        self.webview = QWebEngineView()
        self.webview.load(QtCore.QUrl.fromLocalFile('map.html'))

        # 레이아웃 설정
        layout = QVBoxLayout()
        layout.addWidget(self.webview)
        self.setLayout(layout)

메인 애플리케이션을 실행하는 부분을 추가하세요.

python
Copy code
if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MapWidget()
    widget.show()
    sys.exit(app.exec_())