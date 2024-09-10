import sys
import os
import re
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.QtCore import *
import subprocess


# Pfad zum gewünschten Arbeitsverzeichnis # Das Arbeitsverzeichnis festlegen
arbeitsverzeichnis = os.path.expanduser('/usr/share/x-live/welcome/')

#os.chdir(arbeitsverzeichnis)

class Fenster(QWidget):

    @staticmethod
    def com(self,cmd):
        command = cmd.split(" ")
        complete = subprocess.run(command, capture_output=True)
        ergebnis = str(complete.stdout) 
        return ergebnis

    @staticmethod
    def comw(self,cmd):
        command = cmd.split(" ")
        complete = subprocess.Popen(command)

    def comd(self,cmd):
        command = cmd.split(" ")
        complete = subprocess.Popen(command)
      


    def clickBox(self, state):

        if state == QtCore.Qt.Checked:
            cmd="cp ./starter/x-mint-welcome.desktop " + self.home + "/.config/autostart/x-mint-welcome.desktop"
            self.com(self,cmd)
        else:
            cmd="rm " + self.home + "/.config/autostart/x-mint-welcome.desktop " 
            self.com(self,cmd)

    def thunderup_click(self, state):
        if state == QtCore.Qt.Checked:
            cmd="cp ./starter/thunderbird.desktop " + self.home + "/.config/autostart/thunderbird.desktop"
            self.com(self,cmd)
        else:
            cmd="rm " + self.home + "/.config/autostart/thunderbird.desktop " 
            self.com(self,cmd)

    def logonsound_click(self, state):
        if state == QtCore.Qt.Checked:
            cmd="cp ./starter/loginsound.desktop " + self.home + "/.config/autostart/loginsound.desktop"
            self.com(self,cmd)
        else:
            cmd="rm " + self.home + "/.config/autostart/loginsound.desktop"
            self.com(self,cmd)

    def thunderclock_click(self, state):
        if state == QtCore.Qt.Checked:
            if self.clockcmdisset == 0:
                command="xfconf-query -c xfce4-panel --create -p /plugins/plugin-" + self.clockwidget + "/command -s 'thunderbird --calendar' -t string"
                subprocess.check_output(command, shell=True)
            else:
                command="xfconf-query -c xfce4-panel -p /plugins/plugin-" + self.clockwidget + "/command -s 'thunderbird -calendar'"
                subprocess.check_output(command, shell=True)

        else:
            command="xfconf-query -c xfce4-panel -p /plugins/plugin-" + self.clockwidget + "/command -s 'x-mint-calendar'"
            subprocess.check_output(command, shell=True)

    def clockid(self):
        command = "xfconf-query -c xfce4-panel -l | grep /plugin-ids"
        panel = subprocess.check_output(command, shell=True, text=True).split("\n")[0]
        # print("----"+panel+"----")
        command = "xfconf-query -c xfce4-panel -p " + panel + " | grep -E '^.{1,22}$' | grep -E '^.{1,4}$'"
        output = subprocess.check_output(command, shell=True, text=True).split("\n")[:-1]
        q = -1
        for x in output:
            command = "xfconf-query -c xfce4-panel -p /plugins/plugin-" + str(int(x))
            xoutput = subprocess.check_output(command, shell=True, text=True)
            if xoutput.find("clock") != -1:
                q = str(int(x))
        return q
        
    def clockcommand(self):        
        if int(self.clockwidget) != -1:
            command = "xfconf-query -c xfce4-panel -l"
            command_is_set = subprocess.check_output(command, shell=True, text=True).find("/command")
            print("---"+str(command_is_set)+"----")
            output = "kein command"
            if command_is_set != -1:
                self.clockcmdisset = 1
                command = "xfconf-query -c xfce4-panel -p /plugins/plugin-" + str(int(self.clockwidget)) + "/command"
                output = subprocess.check_output(command, shell=True, text=True).split("\n")[0]
            return output
        else:
            self.cb_thunderclock.setDisabled(True)
            output = "kein command"
            return output


    # Hauptprogramm
    def __init__(self):
        super().__init__()
        self.initMe()

    def initMe(self):

        self.toolname = "Willkommen bei X-Mint"
        self.clockcmdisset = 0
        breite = 600
        hoehe = 505
        bts=16
        sts=14
        
        # Beispielpfad mit nur ~
        path_with_tilde = '~'

        # ~ in den vollständigen Pfad auflösen
        self.home = os.path.expanduser(path_with_tilde)
        print(self.home)

        self.ssshell=str("""
            QWidget {
            background:  rgba(250, 250, 250, 255);
            color: black
            }
            QPushButton {
            background: rgba(10, 10, 10, 15);
            color: rgba(25, 25, 25, 255);
            border-radius: 8px;
            border: 1px solid #f0f0f0
            }
            QPushButton:hover {
            color: rgba(25, 25, 25, 255);
            background: rgba(250, 250, 250, 12);
            border-radius: 8px
            }
            """
            )
        self.ssset=str("""
            QWidget {
            background:  rgba(200, 200, 200, 15);
            color: black
            }
            QPushButton {
            border-radius: 5px;
            border: 1px solid #cccccc;
            background-color:  rgba(250, 250, 250, 215);
            color: black
            }
            QPushButton:hover {
            border-radius: 5px;
            background: rgba(0, 0, 0, 212);
            color: white
            }
            """
            )
        self.sssdunkel=str("""
            QWidget {
            background: rgba(20, 20, 20, 155);
            color: white
            }
            QPushButton {
            background: rgba(10, 10, 10, 215);
            color: rgba(250, 250, 250, 255);
            border-radius: 8px;
            border: 1px solid #222222
            }
            QPushButton:hover {
            color: rgba(250, 250, 250, 255);
            background: rgba(250, 250, 250, 12);
            border-radius: 8px
            }
            """
            )
        self.sssgrau=str("""
            QWidget {
            background: rgba(35,37, 46, 255);
            color: white
            }
            QPushButton {
            background: rgba(90, 92, 101, 115);
            color: rgba(250, 250, 250, 255);
            border-radius: 8px;
            border: 1px solid #626262
            }
            QPushButton:hover {
            color: rgba(250, 250, 250, 255);
            background: rgba(250, 250, 250, 12);
            border-radius: 8px
            }
            """
            )
       
        # Darkmode ??
        self.setStyleSheet(self.sssgrau)
        self.background_color()

        self.fw = 180
        fh = 28
        self.fh = 28

        # Ying und yang logo
        self.label_yay = QLabel(self)
        pixmap = QPixmap('./icons/Yin_and_Yang.png')
        self.label_yay.setPixmap(pixmap.scaled(150,150))
        self.label_yay.move(230,230)
        self.label_yay.setStyleSheet("background: rgba(250,250, 250, 0);")

        # Label X-live und Welcome
        self.label1 = QLabel(self)
        pixmap = QPixmap('./icons/willkommen.png')
        self.label1.setPixmap(pixmap.scaled(560,270))
        self.label1.move(20,0)
        self.label1.setStyleSheet("background: rgba(250,250, 250, 0);")

        # Wallpaper wechseln
        self.btn_backg= QPushButton(self,text="Hintergrundbild\nwechseln")
        self.btn_backg.setIcon(QIcon('./icons/computer.svg'))
        self.btn_backg.setIconSize(QtCore.QSize(48,48))
        self.btn_backg.move(380,215)
        self.btn_backg.clicked.connect(lambda:self.comd("xfdesktop-settings"))
        self.btn_backg.setFixedWidth(self.fw)

        # Auflösung ändern
        self.btn_res= QPushButton(self,text="\tAuflösung ändern")
        self.btn_res.setIcon(QIcon('./icons/auflosung1.png'))
        self.btn_res.setIconSize(QtCore.QSize(48,48))
        self.btn_res.move(20,280)
        self.btn_res.clicked.connect(lambda:self.comd("xfce4-display-settings"))
        self.btn_res.setFixedWidth(self.fw)

        # FireWall einrichten
        self.btn_gufw= QPushButton(self,text="Firewall einrichten")
        self.btn_gufw.setIcon(QIcon('./icons/gufw.png'))
        self.btn_gufw.setIconSize(QtCore.QSize(48,48))
        self.btn_gufw.move(410,280)
        self.btn_gufw.clicked.connect(lambda:self.comd("gufw"))
        self.btn_gufw.setFixedWidth(self.fw)

        # Nvidia und treiber
        self.btn_driver= QPushButton(self,text="Nvidia oder\nzusätzlicher Treiber")
        self.btn_driver.setIcon(QIcon('./icons/nvidia.png'))
        self.btn_driver.setIconSize(QtCore.QSize(48,48))
        self.btn_driver.move(50,215)
        self.btn_driver.clicked.connect(lambda:self.comd("driver-manager"))
        self.btn_driver.setFixedWidth(self.fw)

        # Drucker
        self.btn_printer= QPushButton(self,text="Drucker einrichten")
        self.btn_printer.setIcon(QIcon('./icons/printer.svg'))
        self.btn_printer.setIconSize(QtCore.QSize(48,48))
        self.btn_printer.move(40,345)
        self.btn_printer.clicked.connect(lambda:self.comd("system-config-printer"))
        self.btn_printer.setFixedWidth(self.fw)

        # Backup
        self.btn_update= QPushButton(self,text="Sicherung erstellen")
        self.btn_update.setIcon(QIcon('./icons/timeshift.svg'))
        self.btn_update.setIconSize(QtCore.QSize(48,48))
        self.btn_update.move(390,345)
        self.btn_update.clicked.connect(lambda:self.comd("timeshift-launcher"))
        self.btn_update.setFixedWidth(self.fw)

        # Updatechek
        self.btn_update= QPushButton(self,text=" Updates prüfen")
        self.btn_update.setIcon(QIcon('./icons/update.png'))
        self.btn_update.setIconSize(QtCore.QSize(48,48))
        self.btn_update.move(55,405)
        self.btn_update.clicked.connect(lambda:self.comd("/usr/bin/mintupdate"))
        self.btn_update.setFixedWidth(self.fw)

        # Softwarecenter
        self.btn_software= QPushButton(self,text="Software Center")
        self.btn_software.setIcon(QIcon('./icons/softwarecenter.svg'))
        self.btn_software.setIconSize(QtCore.QSize(48,48))
        self.btn_software.move(375,405)
        self.btn_software.clicked.connect(lambda:self.comd("mintinstall"))
        self.btn_software.setFixedWidth(self.fw)

        # Layout
        self.btn_layout= QPushButton(self,text="\tSystem\n\tanpassen")
        self.btn_layout.setIcon(QIcon('./icons/layout.png'))
        self.btn_layout.setIconSize(QtCore.QSize(48,48))
        self.btn_layout.move(242,405)
        self.btn_layout.clicked.connect(lambda:self.comd("x-mint-settings"))
        self.btn_layout.setFixedWidth(int(self.fw*0.7))


        # über
        self.btn_uber= QPushButton(self,text="über")
        self.btn_uber.setIcon(QIcon('./icons/logo.png'))
        self.btn_uber.setIconSize(QtCore.QSize(22,22))
        self.btn_uber.move(500,5)
        self.btn_uber.clicked.connect(self.show_about_dialog)
        self.btn_uber.setFixedWidth(90)

        # bei start öffnen
        self.cb_startup = QCheckBox("Beim Start öffnen",self)
        if os.path.isfile(self.home + '/.config/autostart/x-mint-welcome.desktop'):
            self.cb_startup.setChecked(True)
        self.cb_startup.move(15,470)
        self.cb_startup.stateChanged.connect(self.clickBox)

        # bei login sound  
        self.cb_loginsound = QCheckBox("Startsound",self)
        if os.path.isfile(self.home + '/.config/autostart/loginsound.desktop'):
            self.cb_loginsound.setChecked(True)
        self.cb_loginsound.move(155,470)
        self.cb_loginsound.stateChanged.connect(self.logonsound_click)

        # bei thunderbird autostart 
        self.cb_thunderup = QCheckBox("Thunderbird Autostart",self)
        if os.path.isfile(self.home + '/.config/autostart/thunderbird.desktop'):
            self.cb_thunderup.setChecked(True)
        self.cb_thunderup.move(250,470)
        self.cb_thunderup.stateChanged.connect(self.thunderup_click)

        # bei Thunderbird Uhr Integration
        self.cb_thunderclock = QCheckBox("Thunderbird-KalenderUhr",self)
        self.clockwidget = self.clockid()
        if self.clockcommand().find("thunderbird -calendar") != -1:
            self.cb_thunderclock.setChecked(True)
        self.cb_thunderclock.move(415,470)
        self.cb_thunderclock.stateChanged.connect(self.thunderclock_click)

        self.label = QLabel(self)
        pixmap = QPixmap('./icons/x-mint.png')
        self.label.setPixmap(pixmap.scaled(450,119))
        self.label.setStyleSheet("background: rgba(250,250, 250, 0);")
        self.label.move(75,100)

        # Fenster anzeigen
        x = int(app.desktop().width()/2-int(breite/2))
        y = int((app.desktop().height()-int(hoehe))/4*3)
        self.setGeometry(x, y, breite, hoehe)
        self.setFixedSize(breite,hoehe)
        self.setWindowTitle(self.toolname)
        self.setWindowIcon(QIcon("./icons/logo.png"))
       
        self.show()

        # Timer erstellen und mit der update-Funktion verbinden
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        
        # Intervall des Timers in Millisekunden festlegen (hier 1000 ms = 1 Sekunde)
        self.timer.start(1000)



    def update(self):
        # Diese Funktion wird aufgerufen, wenn das Fenster den Fokus erhält
        #x=self.com(self,"xfconf-query -c xsettings -p /Net/ThemeName")

        #self.setStyleSheet(self.ssshell)
        #if x.find("Dark") > -1:            
        #    self.setStyleSheet(self.sssgrau)

        #if x.find("Darkest") > -1:            
            #self.setStyleSheet(self.sssdunkel)
        self.background_color()
            
            
    def hex_to_rgb(self,hex_code):
        # Überprüfen, ob der Farbcode mit # beginnt
        if hex_code.startswith('#'):
            hex_code = hex_code[1:]  # Entferne das #
        
        # Sicherstellen, dass der Farbcode 6 Zeichen lang ist
        if len(hex_code) != 6:
            raise ValueError("Der Hex-Farbcode muss 6 Zeichen lang sein, nachdem das # entfernt wurde.")
        
        # Wandeln in RGB um
        r = int(hex_code[0:2], 16)
        g = int(hex_code[2:4], 16)
        b = int(hex_code[4:6], 16)
        
        return f"{r}, {g}, {b}"
        
        
        
        
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
                bcolor = self.extract_color_from_css(css_file_path, ' background-color')
                color = self.extract_color_from_css(css_file_path, ' color')
                
                self.setStyleSheet(str("""
                                    QWidget {
                                    background: rgba("""+self.hex_to_rgb(bcolor)+""", 255);
                                    color: """+color+""";
                                    }
                                    QPushButton {
                                    background: rgba("""+self.hex_to_rgb(color)+""", 125);
                                    color: """+bcolor+""";
                                    border-radius: 8px;
                                    border: 1px solid rgba("""+self.hex_to_rgb(color)+""", 125);
                                    }
                                    QPushButton:hover {
                                    color: """+color+""";
                                    background: rgba("""+self.hex_to_rgb(bcolor)+""", 12);
                                    border-radius: 8px;
                                    border: 1px solid rgba("""+self.hex_to_rgb(color)+""", 52);
                                    }
                                    """
                                    ))
            else:
                print(f"CSS file not found: {css_file_path}")
                return None
        else:
            print("Unable to determine the current theme.")
            return None


    def show_about_dialog(self):
        # Extrahiere die Version aus dem apt show-Befehl
        version = self.get_version_info()
        
        # Über Fenster anzeigen
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Über X-Mint Welcome")
        msg_box.setTextFormat(Qt.RichText)  # Setze den Textformatierungsmodus auf RichText (HTML)
        msg_box.setText(f"X-Mint Welcome<br><br>"
                        f"Autor: VerEnderT aka F. Maczollek<br>"
                        f"Webseite: <a href='https://github.com/verendert/x-mint-welcome'>https://github.com/verendert/x-mint-welcome</a><br>"
                        f"Version: {version}<br><br>"
                        f"Copyright © 2023 - 2024 VerEnderT<br>"
                        f"Dies ist freie Software; Sie können es unter den Bedingungen der GNU General Public License Version 3 oder einer späteren Version weitergeben und/oder modifizieren.<br>"
                        f"Dieses Programm wird in der Hoffnung bereitgestellt, dass es nützlich ist, aber OHNE JEDE GARANTIE; sogar ohne die implizite Garantie der MARKTGÄNGIGKEIT oder EIGNUNG FÜR EINEN BESTIMMTEN ZWECK.<br><br>"
                        f"Sie sollten eine Kopie der GNU General Public License zusammen mit diesem Programm erhalten haben. Wenn nicht, siehe <a href='https://www.gnu.org/licenses/'>https://www.gnu.org/licenses/</a>.")
        msg_box.setIcon(QMessageBox.Information)
        msg_box.exec_()


    def get_version_info(self):
        try:
            result = subprocess.run(['apt', 'show', 'x-live-taskmanager'], capture_output=True, text=True)
            for line in result.stdout.splitlines():
                if line.startswith('Version:'):
                    return line.split(':', 1)[1].strip()
        except Exception as e:
            print(f"Fehler beim Abrufen der Version: {e}")
        return "Unbekannt"


app = QApplication(sys.argv)
w = Fenster()
sys.exit(app.exec())
