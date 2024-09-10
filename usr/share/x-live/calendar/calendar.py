import sys
import os
import subprocess
import re
from PyQt5.QtWidgets import QApplication, QMainWindow, QCalendarWidget, QVBoxLayout, QWidget, QPushButton, QHeaderView
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QPalette, QColor, QIcon

class CalendarApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("X-Mint Kalender")
        self.setWindowIcon(QIcon("/usr/share/x-live/logo.png"))

        # Größe auf 35% der Bildschirmbreite und 50% der Bildschirmhöhe einstellen
        screen_geometry = QApplication.desktop().screenGeometry()
        width = screen_geometry.width() * 0.35
        height = screen_geometry.height() * 0.50
        self.setGeometry(
            int((screen_geometry.width() - width) / 2),
            int((screen_geometry.height() - height) / 2),
            int(width),
            int(height)
        )

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)
        self.calendar = QCalendarWidget(self)

        # Zeige Gitterlinien im Kalender
        #self.calendar.setGridVisible(True)

        # Hintergrundfarbe des aktuellen Datums auf mintgrün setzen
        self.bcolor = "#000000"
        self.color = "#afafaf"
        self.background_color()
        self.central_widget.setStyleSheet("""   QWidget {background-color: """+self.bcolor+""";color: """+ self.color+""";}""")
        self.calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)  # Deaktiviert die Wochennummern  

        self.central_widget.setStyleSheet(f"background-color: {self.bcolor};color: {self.color}")
        # Format für alle Wochentage setzen (weil Wochennummern für die Wochentage festgelegt werden)
        for day in range(Qt.Monday, Qt.Sunday + 1):
            week_format = self.calendar.weekdayTextFormat(day)
            week_format.setBackground(QColor(self.bcolor))  # Hintergrundfarbe setzen
            self.calendar.setWeekdayTextFormat(day, week_format)
        self.layout.addWidget(self.calendar)

        # Heute-Button hinzufügen und mit aktuellem Datum beschriften
        self.today_button = QPushButton(self.get_today_label(), self)
        self.today_button.clicked.connect(self.go_to_today)
        self.layout.addWidget(self.today_button)

    def get_today_label(self):
        # Aktuelles Datum als Beschriftung für den "Heute"-Button zurückgeben
        today = QDate.currentDate()
        return f"Heute: {today.toString('dd.MM.yyyy')}"

    def go_to_today(self):
        # Zurück zum heutigen Tag springen
        today = QDate.currentDate()
        self.calendar.setSelectedDate(today)
        self.today_button.setText(self.get_today_label())  # Aktualisiere die Beschriftung
        
    # Farbprofil abrufen und anwenden

    def get_current_theme(self):
        try:
            # Versuche, das Theme mit xfconf-query abzurufen
            result = subprocess.run(['xfconf-query', '-c', 'xsettings', '-p', '/Net/ThemeName'], capture_output=True, text=True)
            theme_name = result.stdout.strip()
            if theme_name:
                return theme_name
        except FileNotFoundError:
            print("xfconf-query nicht gefunden. Versuche gsettings.")
        except Exception as e:
            print(f"Error getting theme with xfconf-query: {e}")

        try:
            # Fallback auf gsettings, falls xfconf-query nicht vorhanden ist
            result = subprocess.run(['gsettings', 'get', 'org.gnome.desktop.interface', 'gtk-theme'], capture_output=True, text=True)
            theme_name = result.stdout.strip().strip("'")
            if theme_name:
                return theme_name
        except Exception as e:
            print(f"Error getting theme with gsettings: {e}")

        return None

    def extract_color_from_css(self,css_file_path, color_name):
        try:
            with open(css_file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                #print(content)
                # Muster zum Finden der Farbe
                pattern = r'{}[\s:]+([#\w]+)'.format(re.escape(color_name))
                match = re.search(pattern, content)
                if match:
                    return match.group(1)
                return None
        except IOError as e:
            print(f"Error reading file: {e}")
            return None
            
            
    def background_color(self):
        theme_name = self.get_current_theme()
        if theme_name:
            #print(f"Current theme: {theme_name}")

            # Pfad zur GTK-CSS-Datei des aktuellen Themes
            css_file_path = f'/usr/share/themes/{theme_name}/gtk-3.0/gtk.css'
            if os.path.exists(css_file_path):
                self.bcolor = self.extract_color_from_css(css_file_path, ' background-color')
                self.color = self.extract_color_from_css(css_file_path, ' color')
                
            else:
                print(f"CSS file not found: {css_file_path}")
                return None
        else:
            print("Unable to determine the current theme.")
            return None

         
           
                

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CalendarApp()
    window.show()
    sys.exit(app.exec_())
