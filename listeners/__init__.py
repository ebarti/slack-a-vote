from listeners import actions, events, shortcuts, views


def register_listeners(app):
    actions.register(app)
    events.register(app)
    shortcuts.register(app)
    views.register(app)
