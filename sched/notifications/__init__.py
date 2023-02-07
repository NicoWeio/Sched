# TODO: This is a quick hack to prevent crashes on systems without GObject Introspection.
try:
    from .gi import notify
except ImportError:
    print("Could not setup gi's Notify, falling back to print")

    def notify(summary, body=None, icon=None, timeout=None, urgency=None):
        print(f"Notification: {summary} {body}")
