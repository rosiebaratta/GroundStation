from python_qt_binding import loadUi
from PyQt4.Qt import *

try:
    from PyQt4.QtCore import QString
except ImportError:
    QString = type("")

import os
import map_info_parser

PWD = os.path.dirname(os.path.abspath(__file__))

class WpWindow(QWidget):
    def __init__(self, _marble_map, uifname = 'wp_window.ui'):
        super(WpWindow, self).__init__()
        self._marble_map = _marble_map
        ui_file = os.path.join(PWD, 'resources', uifname)
        loadUi(ui_file, self)
        self.setObjectName(uifname)

        self._home_map = self._marble_map._home_map
        self.waypoints = map_info_parser.get_waypoints(self._home_map)

        i = 0
        for waypoint in self.waypoints:
            self.listWidget.addItem(QString(str(i)+': '+str(waypoint)))
            self.comboBox.addItem(QString(str(i)))
            i += 1
        self.comboBox.addItem(QString(str(i)))

        self.pushButton.clicked.connect(self.add_waypoint)
        self.pushButton_2.clicked.connect(self.remove_waypoint)
        # For signal handling
        self._marble_map.WPH.wp_clicked.connect(self.clicked_waypoint)
        self._marble_map.WPH.home_changed.connect(self.change_home)

    def update_lists(self):
        self.listWidget.clear()
        self.comboBox.clear()
        i = 0
        for waypoint in self.waypoints:
            self.listWidget.addItem(QString(str(i)+': '+str(waypoint)))
            self.comboBox.addItem(QString(str(i)))
            i += 1
        self.comboBox.addItem(QString(str(i)))

    def save_waypoints(self):
        wp_file_path = os.path.join(PWD, 'resources', 'wp_data', '%s_wp_data.txt' % self._home_map)
        with open(wp_file_path, 'w') as wp_file:
            for wp in self.waypoints:
                wp_file.write('%f %f %f\n' % (wp[0], wp[1], wp[2]))

    def transfer_waypoint_data(self):
        print('transfer functionality pending')
        # ...
        # ...
        # ...

    def add_waypoint(self):
        # Check PARAMS and emit signal
        try:
            lat = float(str(self.textEdit.toPlainText()))
            lon = float(str(self.textEdit_2.toPlainText()))
            alt = float(str(self.textEdit_3.toPlainText()))
            pos = int(str(self.comboBox.currentText()))
            self.waypoints.insert(pos, (lat, lon, alt))
            self.update_lists()
            self._marble_map.WPH.emit_inserted(lat, lon, alt, pos)
            self.transfer_waypoint_data()
        except ValueError:
            print('Incorrectly formatted fields. Must all be numbers.')

    def remove_waypoint(self):
        pos = self.listWidget.currentRow()
        if pos > -1:
            del self.waypoints[pos]
            self.update_lists()
            self._marble_map.WPH.emit_removed(pos)
            self.transfer_waypoint_data()

    def clicked_waypoint(self, lat, lon):
        self.textEdit.setText(QString(str(lat)))
        self.textEdit_2.setText(QString(str(lon)))

    def change_home(self, new_home):
        self.save_waypoints()
        self.waypoints = map_info_parser.get_waypoints(new_home)
        self.update_lists()
        self._home_map = new_home

    def closeEvent(self, QCloseEvent):
        self.save_waypoints()
        self._marble_map.setInputEnabled(True)
        self._marble_map._mouse_attentive = False
