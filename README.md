## Blick auf die Konkurrenz

-   _cron_ ist natürlich der Standard. Wenn ich aber z.B. Täglich um 16 Uhr einen Job ausführen möchte, den PC aber erst um 20 Uhr einschalte, wird der Job nicht ausgeführt.

-   _anacron_ löst dieses Problem, benachrichtigt aber wie auch _cron_ nur per E-Mail. Empfehlung in diesem Zusammenhang: _nullmailer_.

-   _jobber_ hat ein nettes CLI und geht super mit Fehlern um (Benachrichtigungen, exponential backoff, …). Leider fehlt die _anacron_-Funktionalität und das Projekt ist seit einer Weile nicht mehr aktiv.
