# TMail

A lightweight command-line SMTP email utility for sending emails and attachments directly from the terminal.

TMail stores SMTP credentials in the current user's home directory and supports sending individual emails to multiple recipients without exposing recipient addresses via CC or BCC.

---

## Features

* Simple SMTP configuration wizard
* Store credentials in `~/.tmail.config`
* Send plain text emails
* Send attachments
* Multiple recipients supported
* Each recipient receives a separate email
* User-local installation (no root privileges required)

---

## Installation

Clone or download the project files:

```text
tmail/
├── tmail.py
└── install.sh
```

Run the installer:

```bash
chmod +x install.sh
./install.sh
```

The installer will:

* Copy the utility to:

```text
~/.local/bin/tmail
```

* Make it executable
* Add `~/.local/bin` to your PATH if necessary

Open a new terminal session or reload your shell:

```bash
source ~/.bashrc
```

or

```bash
source ~/.zshrc
```

---

## Configuration

Before sending email, configure your SMTP account:

```bash
tmail config
```

You will be prompted for:

```text
SMTP host
SMTP port
SMTP username/email
SMTP password
Use TLS
```

Example:

```text
SMTP host: smtp.gmail.com
SMTP port: 587
SMTP username/email: myaccount@gmail.com
SMTP password: ********
Use TLS: y
```

The configuration is stored in:

```text
~/.tmail.config
```

with permissions:

```text
600
```

so only the current user can read it.

---

## Sending Email

### Single Recipient

```bash
tmail send \
    --subject "Hello" \
    --message "Testing TMail" \
    --to user@example.com
```

### Multiple Recipients

```bash
tmail send \
    --subject "Weekly Report" \
    --message "Please see attached." \
    --to alice@example.com \
    --to bob@example.com \
    --to charlie@example.com
```

Each recipient receives an independent email.

---

## Sending Attachments

Attach one or more files:

```bash
tmail send \
    --subject "Documents" \
    --message "Attached are the requested files." \
    --to user@example.com \
    --file report.pdf \
    --file invoice.xlsx \
    --file image.png
```

---

## Command Reference

### Configure SMTP

```bash
tmail config
```

### Send Email

```bash
tmail send \
    --subject SUBJECT \
    --message MESSAGE \
    --to RECIPIENT \
    [--to RECIPIENT ...] \
    [--file FILE ...]
```

### Arguments

| Argument    | Description                    |
| ----------- | ------------------------------ |
| `--subject` | Email subject                  |
| `--message` | Plain text email body          |
| `--to`      | Recipient address (repeatable) |
| `--file`    | Attachment path (repeatable)   |

---

## Example

```bash
tmail send \
    --subject "Deployment Complete" \
    --message "The latest release has been deployed successfully." \
    --to dev1@example.com \
    --to dev2@example.com \
    --file deployment.log
```

---

## Gmail Users

Google generally requires an App Password instead of your normal account password.

1. Enable Two-Factor Authentication on your Google account.
2. Generate an App Password.
3. Use the generated password when running:

```bash
tmail config
```

Typical Gmail settings:

```text
Host: smtp.gmail.com
Port: 587
TLS: Yes
```

---

## Security Notes

* SMTP credentials are stored locally in:

```text
~/.tmail.config
```

* The file permissions are automatically set to:

```text
600
```

* Avoid committing configuration files to version control.
* Consider using dedicated SMTP accounts or app passwords for automation.

---

## License

MIT License.

Use at your own risk. Always verify SMTP credentials and attachment contents before sending mail.
