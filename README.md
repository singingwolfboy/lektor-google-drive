# lektor-google-drive

Lektor-Google-Drive adds a `google-drive` field type to
[Lektor](https://www.getlektor.com/), allowing you to embed the contents of
a Google Document into your static website.

Model:
```ini
[fields.document]
label = Google Drive document ID
type = google-drive
```

Content:
```ini
document: 1aDDm7shDaA9e_TVbpL1NGHwj6K5smInqJsXmVoOPCGE
```

Template:
```jinja
<h1>{{ this.document.title }}</h1>
<p>{{ this.document.text }}</p>
OR
{{ this.document.html }}
```

## Configuration

In order to use this plugin, you must create an application on the
[Google Developers Console](https://console.developers.google.com/). Enable
the [Drive API](https://console.developers.google.com/apis/api/drive),
and create a credential to access it. The credential should be an OAuth client
ID, with type set to "Other". Google will give you an OAuth client ID and
client secret, which Lektor needs in order to access the API.

In your Lektor project, create a file at `configs/google-drive.ini`, with
the following content:

```ini
[api]
client_id = <CLIENT_ID>
client_secret = <CLIENT_SECRET>
```

You'll need to replace `<CLIENT_ID>` and `<CLIENT_SECRET>` with the values you
got from the Google Developers Console when setting up your credential.

## Authorization

This plugin uses the [Google Drive API](https://developers.google.com/drive/v3/web/about-sdk)
to fetch information about the document. This API requires OAuth 2.0 to
authorize requests, and right now, the workflow is a little janky. Every time
you build your app, Lektor will open an OAuth consent page in your web browser,
and ask you to copy-paste the code that Google gives you. This is a terrible
user experience, and it should be improved. Ideas and pull requests are welcome!

There is a hacky workaround: once you get an OAuth access token from Google
by going through the OAuth dance, you can save it in your `google-drive.ini`
file under the `[api]` heading, with the `access_token` key. However, access
tokens are short-lived, so this is not a good solution to this problem, merely
a temporary hack. Do not rely on it! It *will* be removed from future versions
of this plugin.
