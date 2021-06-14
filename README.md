This simple script allows you to "cycle" your Discord profile status periodically. It has no external dependencies, and supports both default and custom emojis. 

As of right now the API doesn't seem to impose any sort of rate-limitation, but I fully expect that to change in the future.

# Quickstart

1. Obtain the script (either clone the repository or download the file directly)
2. Obtain a Discord authentication token of your account (it's commonly found as an `"Authorization"` header value in many requests - take a look at the devtools)
3. Run the script: 

```sh
$ cycler.py <auth_token> <status_combo_1> <status_combo_2> [...]
```

`<auth_token>` is your personal authentication token. Every commandline argument after that represents a status combo formed of 3 strings (delimited by colons (`:`)), in the following form:

```
<status_text>:<emoji_name>:<emoji_id>
```

* `<status_text>` is the actual text of your status - it is optional
* `<emoji_name>` is the *name* of the emoji to the left of the status text
* `<emoji_id>` is the internal Discord ID of the emoji you're trying to use, and is only required for custom (*non-default*) emojis

Example CLI: `$ cycler.py <token> how:grin: you:grin: doin?:bean:801184256202113054`

---

Once the script is run, it will indefinitely cycle between all provided status combos. The default wait time between requests is `1` second. If a network error occurs, the delay time is increased
by `1` second. After a successful request occurs after many failed attempts, the delay time is reset back to `1` second.

### Caveat concerning custom emoji IDs

The IDs of the custom emojis are in fact ***not*** the ones provided by the Discord "Developer mode" Copy-ID action from the UI. In order to obtain the correct ID of a custom emoji, you need to: 

1. Clear your status and make sure the script is not running
2. Open the devtools and select the "Network" tab
3. Set your status manually from within the Discord UI, choosing the appropriate custom emoji
4. Observe the appropriate request in the "Network" tab (the Chrome devtools shorten its URL to `settings`) and select it
5. Observe the correct `emoji_id` value in the JSON request payload of the request

### `systemd` service unit for autostarting on linux systems

You can use and enable the following `systemd` unit in order to autostart the script when you start your machine.

1. Copy the following contents to `/etc/systemd/system/discord_statuscycle.service`

```
[Unit]
Description=Autostart and manage the discord status cycler
Wants=network-online.target
After=network-online.target

[Service]
ExecStart=<FULL_CLI_GOES_HERE>

[Install]
WantedBy=multi-user.target
```

2. Run `$ systemctl enable discord_statuscycle.service`
3. Run `$ systemctl start discord_statuscycle.service`
4. If you ever change the unit file (e.g. to modify the status combos), run `$ systemctl daemon-reload` followed by `$ systemctl restart discord_statuscycle.service` for the changes to take effect.
