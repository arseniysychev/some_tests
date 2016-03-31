import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class HTMLEmail(object):
    """
    Object for sending HTML email.

    For __init__():
    * main params
        host - host for sending

    * additional params
        port - port for sending
        images_dir - dir for get images
        template_text - file or string
            "Dear, {user_name} \nHello world!"
        template_html - file or string
            "<div>
                <p>Dear, {user_name}</p>
                <p>Hello world!</p>
                <a href="http://link.com/">Link</a>
                <img src="cid:image_name.jpeg">
            </div>"
        auth - dict for SMTP auth (user='', password='')
        charset - charset for email
        format - format template for generate title name

    For send():
    * main params
        context - context for template as dict
        subject - subject for email
        sender - from email
        recipient - to email
    * additional params
        sender_name - name for sender
        recipient_name - name for recipient
        images - images list for sending
    """

    port = 0
    auth = dict(user=None, password=None)
    charset = 'utf-8'
    format = '{name} <{mail}>'
    template_text = ''
    template_html = None
    images_dir = ''

    def __init__(self, host, **kwargs):
        self.host = host

        for kw, value in kwargs.items():
            setattr(self, kw, value)

    def formatting(self, template, context):
        try:
            with open(template) as template_file:
                text = template_file.read()
                text = text.format(**context)
        except IOError:
            text = template.format(**context)
            if not text:
                return str(context)
        return text

    def send(self, context, subject, sender, recipient, **kwargs):

        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = self._named(sender, kwargs.get('sender_name'))
        msg['To'] = self._named(recipient, kwargs.get('recipient_name'))

        text = self.formatting(self.template_text, context)

        if self.template_html:
            html = self.formatting(self.template_html, context)
            msg.attach(MIMEText(html, 'html', _charset=self.charset))

        msg.attach(MIMEText(text, 'plain', _charset=self.charset))

        if 'images' in kwargs:
            for img in kwargs['images']:
                img_path = '{dir}/{img}'.format(
                    dir=self.images_dir.rstrip('/'),
                    img=img)

                with open(img_path, 'rb') as file_picture:
                    msg_image = MIMEImage(file_picture.read())
                    msg_image.add_header(
                        _name='Content-ID',
                        _value='<{img}>'.format(img=img),
                    )

                msg.attach(msg_image)

        self._send(sender, recipient, msg)

    def _send(self, sender, recipient, msg):
        mail = smtplib.SMTP(self.host, self.port)
        mail.starttls()
        mail.login(**self.auth)
        mail.sendmail(sender, recipient, msg.as_string())
        mail.quit()

    def _named(self, mail, name, **kwargs):
        if name:
            return self.format.format(name=name, mail=mail)
        return mail
