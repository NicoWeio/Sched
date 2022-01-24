## Features

-   Erfordert nicht, dass der PC/Server ständig eingeschaltet ist. (→ wie Anacron)
-   Maximale Ausführungszeit (Option `time_limit`)
-   Error-Handling
    - [ ] Nicht erneut versuchen
    - [ ] Konfigurierbare Wartezeit
        - Wartet bislang eine Stunde, bis fehlgeschlagene Jobs erneut ausgeführt werden.
    - [ ] Exponential backoff
-   Benachrichtigungen
    - Desktop (`notify-send`)
    - [ ] E-Mail (bislang nur indirekt über `crontab`)
-   Klein und übersichtlich.
-   Geschrieben in Python. :)

## Einrichtung

Wichtig ist nur, dass die `main.py` von Sched regelmäßig ausgeführt wird.
Das kann zum Beispiel über einen `crontab`-Eintrag erreicht werden:

    * * * * * /path/to/Sched/main.py > /dev/null

### Systemd-Daemon
Der Systemd-Daemon verhindert z.B. den Log-Spam von `cron`.
TODO: `--user`-Flag?
```shell
systemctl --user link $(realpath sched_daemon.service) # zu Debug-Zwecken
# systemctl --user daemon-reload
# Prüfe, ob alles funktioniert:
systemctl --user start sched_daemon.service
systemctl --user status sched_daemon.service
# Funktioniert? Dann „permanent“ starten:
systemctl --user enable sched_daemon.service
```

## Blick auf die Konkurrenz

-   _cron_ ist natürlich der Standard. Wenn ich aber z.B. täglich um 16 Uhr einen Job ausführen möchte, den PC aber erst um 20 Uhr einschalte, wird der Job nicht ausgeführt.

-   _anacron_ löst dieses Problem, benachrichtigt aber wie auch _cron_ nur per E-Mail. Empfehlung in diesem Zusammenhang: _nullmailer_.

-   _jobber_ hat ein nettes CLI und geht super mit Fehlern um (Benachrichtigungen, exponential backoff, …). Leider fehlt die _anacron_-Funktionalität und das Projekt ist seit einer Weile nicht mehr aktiv.
