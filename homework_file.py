from datetime import datetime

from email_list import (
    email1,
    email2,
    email3,
    email4,
    email5,
    test_emails,
    test_working_emails,
)


def normalize_addresses(value: str) -> str:
    """
    Возвращает значение, в котором адрес приведен
    к нижнему регистру и очищен от пробелов по краям.
    """
    return value.strip().lower()


def add_short_body(email: dict) -> dict:
    """
    Возвращает email с новым ключом email["short_body"] —
    первые 10 символов тела письма + "...".
    """
    short_body = email["body"][:10]
    if short_body == "":
        email["short_body"] = "Empty message"
    else:
        email["short_body"] = f"{short_body}..."
    return email


def clean_body_text(body: str) -> str:
    """
    Заменяет табы и переводы строк на пробелы.
    """
    return body.replace("\t", " ").replace("\n", " ")


def build_sent_text(email: dict) -> str:
    """
    Формирует текст письма в формате:

    Кому: {to}, от {from}
    Тема: {subject}, дата {date}
    {clean_body}
    """
    send_date = datetime.now().strftime("%Y-%m-%d")
    email["subject"] = email["subject"].strip()
    return (
        f"From: {email["sender"]}\nTo: {email["recipient"]}\nSubject:"
        f" {email["subject"]}\nData: {send_date}\n"
        f"{email["body"]}"
    )


def check_empty_fields(subject: str, body: str) -> tuple[bool, bool]:
    """
    Возвращает кортеж (is_subject_empty, is_body_empty).
    True, если поле пустое.
    """
    return not subject, not body


def mask_sender_email(login: str, domain: str) -> str:
    """
    Возвращает маску email: первые 2 символа логина + "***@" + домен.
    """
    return f"{login[:2]}***@{domain}"


def get_correct_email(email_list: list[str]) -> list[str]:
    """
    Возвращает список корректных email.
    """
    correct_emails = []
    for email in email_list:
        email = email.strip()
        if "@" in email:
            name, domain = (
                email.split("@")[0].lower(),
                email.split("@")[1].lower(),
            )
            if "." in domain:
                left_domain, right_domain = domain.rsplit(".", 1)
                if name != "" and left_domain != "" and right_domain != "":
                    if right_domain in ["com", "ru", "net"]:
                        correct_emails.append(email)
    return correct_emails


def create_email(sender: str, recipient: str, subject: str, body: str) -> dict:
    """
    Создает словарь email с базовыми полями:
    'sender', 'recipient', 'subject', 'body'
    """
    email = {
        "sender": sender,
        "recipient": recipient,
        "subject": subject,
        "body": body,
    }
    return email


def add_send_date(email: dict) -> dict:
    """
    Возвращает email с добавленным ключом email["date"] —
    текущая дата в формате YYYY-MM-DD.
    """
    email["date"] = datetime.now().strftime("%Y-%m-%d")
    return email


def extract_login_domain(address: str) -> tuple[str, str]:
    """
    Возвращает логин и домен отправителя.
    Пример: "user@mail.ru" -> ("user", "mail.ru")
    """
    return address.split("@")[0], address.split("@")[1]


def sender_email(
    recipient_list: list[str],
    subject: str,
    message: str,
    *,
    sender="default@study.com",
) -> list[dict]:
    if len(recipient_list) == 0:
        raise ValueError("Empty recipient list")
    if len(get_correct_email([sender])) == 0 or len(recipient_list) != len(
        get_correct_email(recipient_list)
    ):
        raise ValueError(
            "Sender email or one of the recipient emails is incorrect"
        )
    clean_recipients = []
    for recipient in recipient_list:
        if recipient != sender:
            clean_recipients.append(recipient)
    subject, message = clean_body_text(subject), clean_body_text(message)
    sender = normalize_addresses(sender)
    normalized_recipients = []
    for email in clean_recipients:
        normalized_recipients.append(normalize_addresses(email))
    print(normalized_recipients)
    list_of_emails = []
    for email in normalized_recipients:
        new_email = create_email(
            sender=sender, recipient=email, subject=subject, body=message
        )
        new_email = add_send_date(new_email)
        address, domain = extract_login_domain(sender)
        new_email["masked_sender"] = mask_sender_email(address, domain)
        new_email = add_short_body(new_email)
        new_email["sent_text"] = build_sent_text(new_email)
        list_of_emails.append(new_email)
    return list_of_emails


# check result
result = sender_email(test_working_emails, email1["subject"], email1["body"])
for i in result:
    for key in i.keys():
        print(key + ": " + i.get(key))
    print("=" * 30)
