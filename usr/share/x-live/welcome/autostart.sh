#!/bin/bash

# Überprüfen, ob das Skript im Live-Modus ausgeführt wird
if [ "$USER" == "live" ]; then
    # Sprache auswählen
    LANGUAGE=$(zenity --list --title="Sprache auswählen / select Language" --column="Sprache/Language" "Deutsch" "English")

    # Spracheinstellungen ändern
    if [ "$LANGUAGE" == "English" ]; then
        killall xfce4-panel &
        export LANG=en_US.UTF-8
        export LANGUAGE=en_US.UTF-8
        export LC_ALL=en_US.UTF-8

        # Sprache in der .profile-Datei setzen
        echo 'export LANG=en_US.UTF-8' >> ~/.profile
        echo 'export LANGUAGE=en_US.UTF-8' >> ~/.profile
        echo 'export LC_ALL=en_US.UTF-8' >> ~/.profile
        killall xfwm4 &
        sleep 5        
        xfce4-panel &
        xfwm4 &

    elif [ "$LANGUAGE" == "Deutsch" ]; then
        killall xfce4-panel &
        export LANG=de_DE.UTF-8
        export LANGUAGE=de_DE.UTF-8
        export LC_ALL=de_DE.UTF-8

        # Sprache in der .profile-Datei setzen
        echo 'export LANG=de_DE.UTF-8' >> ~/.profile
        echo 'export LANGUAGE=de_DE.UTF-8' >> ~/.profile
        echo 'export LC_ALL=de_DE.UTF-8' >> ~/.profile
        killall xfce4-panel &
        killall xfwm4 &
        sleep 5 
        xfce4-panel &
        xfwm4 &
    fi

    # XFCE-Panel und Fenster-Manager neu starten, um die Änderungen zu übernehmen
    
    
else
    # Falls der Benutzer nicht 'live' ist, den Welcome-Screen starten
    x-mint-welcome
fi
