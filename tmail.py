#!/usr/bin/env python3

import argparse
import getpass
import json
import smtplib
from email.message import EmailMessage
from pathlib import Path

CONFIG_PATH = Path.home() / ".tmail.config"


def save_config_interactive():
    print("SMTP Configuration Setup")
    print("------------------------")

    host = input("SMTP host (e.g. smtp.gmail.com): ").strip()
    port = input("SMTP port (e.g. 587): ").strip() or "587"
    user = input("SMTP username/email: ").strip()
    password = getpass.getpass("SMTP password (hidden): ").strip()
    use_tls = input("Use TLS? (y/n) [y]: ").strip().lower() or "y"

    config = {
        "host": host,
        "port": int(port),
        "user": user,
        "password": password,
        "use_tls": use_tls in ("y", "yes", "true", "1"),
    }

    CONFIG_PATH.write_text(json.dumps(config, indent=2))
    CONFIG_PATH.chmod(0o600)

    print(f"\nSaved config to {CONFIG_PATH}")


def load_config():
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"No config found. Run: tmail.py config")

    return json.loads(CONFIG_PATH.read_text())


def build_message(subject, body, sender, recipient, attachments):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient
    msg.set_content(body)

    for file_path in attachments:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"Attachment not found: {file_path}")

        data = path.read_bytes()
        msg.add_attachment(
            data, maintype="application", subtype="octet-stream", filename=path.name
        )

    return msg


def send_email(config, msg):
    with smtplib.SMTP(config["host"], config["port"]) as server:
        server.ehlo()

        if config.get("use_tls", True):
            server.starttls()
            server.ehlo()

        server.login(config["user"], config["password"])
        server.send_message(msg)


def run_send(args):
    config = load_config()
    sender = config["user"]

    attachments = args.file or []
    processed_recipients: list[str] = []

    for recipient in args.to:
        recipient_ = sender if recipient == "SELF" else recipient

        if recipient_ in processed_recipients:
            continue

        msg = build_message(
            subject=args.subject,
            body=args.message,
            sender=sender,
            recipient=recipient_,
            attachments=attachments,
        )

        send_email(config, msg)
        processed_recipients.append(recipient_)

        print(f"Sent email to {recipient_}")


HELP_MESSAGE = """
tmail config : Configure SMTP credentials
tmail send *args : Send email
    --to -> Receivers, multiple declarations allowed
    --subject -> Message subject
    --message -> Actual message
    --file -> File attachments, takes filepath, multiple declarations allowed
"""


def main():
    parser = argparse.ArgumentParser(description="TMail SMTP CLI tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("config", help="Setup SMTP credentials")
    send = subparsers.add_parser("send", help="Send email")

    send.add_argument("--subject", required=True)
    send.add_argument("--message", required=True)

    send.add_argument(
        "--to", action="append", required=True, help="Recipient email (repeatable)"
    )

    send.add_argument(
        "--file", action="append", default=[], help="Attachment file path (repeatable)"
    )

    args = parser.parse_args()

    if args.command == "config":
        save_config_interactive()

    elif args.command == "send":
        run_send(args)


if __name__ == "__main__":
    main()
