# Mailman event sender

This package is a plugin for [mailman 3](https://docs.mailman3.org/en/latest/) which allows to send webhook-like events to configurable endpoints.

## Configuration

As for every plugin, register it in `mailman.cfg`:

```cfg
[plugin.mailman_rest_event]
class: mailman_rest_event.plugin.RestEventPlugin
enabled: yes
# Or specify your own location
configuration: /etc/mailman3/mailman-rest-event.cfg 
```

Then configure the plugin in `mailman-rest-event.cfg`:

```cfg
[general]
# URL to which events will be sent
webhook_url: https://example.com/mailman/event
# Response timeout for event calls
timeout: 2

# Username and key used to authenticate the URL
# These credentials will be sent as Authorization Basic header
[auth]
user: auth_user
key: auth_key
```