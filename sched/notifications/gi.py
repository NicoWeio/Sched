import gi
gi.require_version('Notify', '0.7')
from gi.repository import Notify

Notify.init('Sched')


def notify(summary, body=None, icon=None, timeout=None, urgency=None):
    n = Notify.Notification.new(summary, body, icon)

    # n.add_action('retry', 'Erneut versuchen', lambda x: print('Yeah!'))
    if timeout:
        n.set_timeout(timeout)
    if urgency:
        n.set_urgency(getattr(Notify.Urgency, urgency))

    success = n.show()
    return success
