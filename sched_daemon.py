#!/usr/bin/env python3
# Diese Datei darf nicht daemon.py heißen, sonst funktioniert der Zauber (natürlich) nicht…

import time

from main import main

while True:
    main()
    time.sleep(60)
