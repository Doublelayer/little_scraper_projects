TOKEN = "token"  # your application's API token (required)
USER = "user"  # your user/group key (or that of your target user), viewable when logged into our dashboard; often referred to as USER_KEY in our documentation and code examples (required)
MESSAGE = "message"  # your message (required)

ATTACHMENT = "attachment"  # a binary image attachment to send with the message
ATTACHMENT_BASE64 = "attachment_base64"  # a Base64-encoded image attachment to send with the message
ATTACHMENT_TYPE = "attachment_type"  # the MIME type of the included attachment or attachment_base64
DEVICE = "device"  # the name of one of your devices to send just to that device instead of all devices
HTML = "html"  # set to 1 to enable HTML parsing
PRIORITY = "priority"  # a value of -2, -1, 0 (default), 1, or 2
SOUND = "sound"  # the name of a supported sound to override your default sound choice
TIMESTAMP = "timestamp"  # a Unix timestamp of a time to display instead of when our API received it
TITLE = "title"  # your message's title, otherwise your app's name is used
TTL = "ttl"  # a number of seconds that the message will live, before being deleted automatically
URL = "url"  # a supplementary URL to show with your message
URL_TITLE = "url_title"  # a title for the URL specified as the url parameter, otherwise just the URL is shown
