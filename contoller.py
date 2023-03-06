import cv2
from src.plugin_interface import PluginInterface
from PyQt6.QtWidgets import QWidget
from .ui_main import Ui_Form


class Controller(QWidget):
    def __init__(self, model):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.model = model
        self.set_stylesheet()
        self.connect_to_button()

    def set_stylesheet(self):
        self.ui.label.setStyleSheet("font-size:44px;")

    def connect_to_button(self):
        self.ui.open_file.clicked.connect(self.onclick_open)

        # setting configuration recenter
        self.ui.doubleSpinBox.valueChanged.connect(self.recenter_image)
        self.ui.doubleSpinBox_2.valueChanged.connect(self.recenter_image)
        self.ui.doubleSpinBox_3.valueChanged.connect(self.recenter_image)

    def onclick_open(self):
        cam_type, media_source, params_name = self.model.select_media_source()
        if cam_type:
            if params_name:
                self.moildev = self.model.connect_to_moildev(parameter_name=params_name)
            self.image_ori = cv2.imread(media_source)
            self.image = self.image_ori.copy()
            self.show_to_ui()
            self.recenter_image()

    def show_to_ui(self):
        map_x, map_y = self.moildev.maps_anypoint_mode2(0, 0, 0, 4)
        draw_img = self.model.draw_polygon(self.image, map_x, map_y)
        self.model.show_image_to_label(self.ui.label_5, draw_img, 900)

    def recenter_image(self):
        alpha_max = self.ui.doubleSpinBox.value()
        ic_alpha = self.ui.doubleSpinBox_2.value()
        ic_beta = self.ui.doubleSpinBox_3.value()

        self.remap = self.moildev.recenter(self.image, alpha_max, ic_alpha, ic_beta)
        self.model.show_image_to_label(self.ui.label_6, self.remap, 900)

class HelloWorld(PluginInterface):
    def __init__(self):
        super().__init__()
        self.widget = None
        self.description = "This is a plugins application"

    def set_plugin_widget(self, model):
        self.widget = Controller(model)
        return self.widget

    def set_icon_apps(self):
        return "icon.png"

    def change_stylesheet(self):
        self.widget.set_stylesheet()

