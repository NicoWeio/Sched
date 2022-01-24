#!/usr/bin/env python3
# Diese Datei darf nicht daemon.py heißen, sonst funktioniert der Zauber (natürlich) nicht…

from main import main
import time


while True:
    main()
    time.sleep(60)
