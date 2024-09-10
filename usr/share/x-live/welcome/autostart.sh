#!/bin/bash

# Überprüfen, ob der aktuelle Benutzer "live" ist
if [ "$(whoami)" != "live" ]; then
    # Programm starten, wenn der Benutzer nicht "live" ist
    x-mint-welcome &
fi
