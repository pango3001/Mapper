import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QLineEdit, QWidget, QFileDialog, QComboBox
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import folium
from folium.plugins import Draw

class MapApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Map Viewer with Polygon Drawing")
        self.setGeometry(100, 100, 1200, 800)

        self.tile_services = {
            "OpenStreetMap": "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
            "Bing Satellite": "https://t.ssl.ak.dynamic.tiles.virtualearth.net/comp/CompositionHandler/{quadkey}?mkt=en-US&it=A,G,L,LA&shading=hill&n=z",
            "Google Satellite": "https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}"
        }

        self.default_tile_service = "OpenStreetMap"
        self.initUI()

    def initUI(self):
        # Main layout
        main_layout = QHBoxLayout()

        # Map view
        self.map_view = QWebEngineView()
        self.create_map(self.tile_services[self.default_tile_service])
        main_layout.addWidget(self.map_view, 2)

        # Control panel
        control_panel = QVBoxLayout()

        # Tile map service selection
        control_panel.addWidget(QLabel("Select Tile Map Service:"))
        self.tile_service_selector = QComboBox()
        self.tile_service_selector.addItems(self.tile_services.keys())
        self.tile_service_selector.setCurrentText(self.default_tile_service)
        self.tile_service_selector.currentIndexChanged.connect(self.change_tile_service)
        control_panel.addWidget(self.tile_service_selector)

        # Save map button
        self.save_map_button = QPushButton("Save Map as HTML")
        self.save_map_button.clicked.connect(self.save_map)
        control_panel.addWidget(self.save_map_button)

        control_panel.addStretch()
        main_layout.addLayout(control_panel, 1)

        # Set main widget
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def create_map(self, tile_service):
        # Generate a folium map
        self.map = folium.Map(location=[0, 0], zoom_start=2, tiles=tile_service, attr="Custom Tile Service")

        # Add drawing tools
        draw = Draw()
        self.map.add_child(draw)

        # Save map to temporary file
        map_file = "map.html"
        self.map.save(map_file)

        # Load map in QWebEngineView
        self.map_view.setUrl(QUrl.fromLocalFile(os.path.abspath(map_file)))

    def change_tile_service(self):
        selected_service = self.tile_service_selector.currentText()
        if selected_service in self.tile_services:
            self.create_map(self.tile_services[selected_service])

    def save_map(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Map", "", "HTML Files (*.html);;All Files (*)", options=options)
        if file_name:
            self.map.save(file_name)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MapApp()
    main_window.show()
    sys.exit(app.exec_())
