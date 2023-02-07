from datetime import datetime

EXAMPLE_CONFIG = {
    'version': '0.0.1',
    'jobs': {
        'example': {
            'command': 'echo "Hello, world!" && sleep 5 && echo "Goodbye, world!"',
            'schedule': '*/5 * * * *',
        },
    },
}

EXAMPLE_SPOOL = {
    'jobs': {
        'example': {
            'status': 'SUCCESS',
            # NOTE: There is a small but important difference between passing datetimes and strings!
            # HACK: We set these datetimes to the UNIX epoch (1970-01-01 00:00:00) to indicate that they have never been set. We should work with None in the future.
            'last_executed': datetime(1970, 1, 1, 0, 0, 0),
            'last_success': datetime(1970, 1, 1, 0, 0, 0),
        },
    },
}
