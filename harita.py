import io
import folium
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
import RotaAlg

zoom_level = 17
class HaritaOlustur(QWidget):
    def __init__(self, coordinate, points, coorsayi):
        super().__init__()
        self.setWindowTitle('Harita')

        x = []
        y = []

        for i in range(len(points)):
            x.append(points[i][0])
            y.append(points[i][1])

        path = RotaAlg.rotaHesapla(x,y)
        # print(path)

        for i in range(len(path)):
           path[i][0] = path[i][0] / 100000
           path[i][1] = path[i][1] / 100000

        layout = QVBoxLayout()
        self.setLayout(layout)

        m = folium.Map(
            title = "ev",
            zoom_start = zoom_level,
            max_zoom=zoom_level,
            location=coordinate)
        folium.PolyLine(points, color="red",popup="Merhaba", weight=6, opacity=1).add_to(m)
        folium.PolyLine(path, color="red", popup="Merhaba", weight=0.5, opacity=1).add_to(m)
        folium.TileLayer(tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                                max_native_zoom=zoom_level,zoom_level = 17 ,attr='Esri',name='Esri Satellite',overlay=False,control=True).add_to(m)

        data = io.BytesIO()
        m.save(data, close_file=False)

        webViev = QWebEngineView()
        webViev.setHtml(data.getvalue().decode())
        layout.addWidget(webViev)
