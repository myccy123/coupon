import yagmail

sender_id = 'JT-cloud@bjjttec.com'
sender_password = 'Yjh932320908'
mail_host = "smtp.exmail.qq.com"


def send_email(to, cc=None, contents=None, subject=''):
    if contents is None:
        contents = []
    if cc is None:
        cc = []
    try:
        yag = yagmail.SMTP(user=sender_id, password=sender_password,
                           host=mail_host)
        yag.send(to=to, cc=cc, contents=contents, subject=subject)
        print(f'send email to {to} successfully!')
    except Exception as e:
        print('send email failed!')
        print(e)
