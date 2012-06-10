import logging

from flaskext.mail import Mail, Message


class MailHandler(logging.Handler):
    """Implements sending email using Flask-Mail"""

    def __init__(self, app, mail, formatter=None):
        logging.Handler.__init__(self)
        self.app = app
        self.mail = mail
        if not isinstance(formatter, logging.Formatter):
            formatter = logging.Formatter('''
Message type:       %(levelname)s
Location:           %(pathname)s:%(lineno)d
Module:             %(module)s
Function:           %(funcName)s
Time:               %(asctime)s

Message:

%(message)s
''')
        self.setFormatter(formatter)

    def get_subject(self, record):
        subject = 'Error in Flask app'
        server_name = self.app.config.get('SERVER_NAME')
        if server_name:
            subject += ' on %s' % server_name
        return subject

    def emit(self, record):
        """
        Format and send logging record as email using Flask-Mail.

        Note that emit will work only in request, since Flask-Mail dependency
         uses request context.
        """
        admins = self.app.config.get('ADMINS')
        if not admins:
            return
        msg = Message(
            subject=self.get_subject(record),
            recipients=[a[1] for a in admins],
            body=self.format(record),
        )
        self.mail.send(msg)


def init_app(app):
    """
    Initialize Flask-Mail and Flask-MailErrors extensions.

    All recipients must be listed as tuples ('Name', 'email@example.net') in
     app.config['ADMINS'] list.
    """
    app.config.setdefault('DEFAULT_MAIL_SENDER', 'webmaster@localhost')
    # prevent adding more than one error mail handler to app.logger
    mail_handler = None
    for handler in app.logger.handlers:
        if isinstance(handler, MailHandler):
            mail_handler = handler
            break
    if mail_handler is None:
        mail = Mail(app)
        mail_handler = MailHandler(app, mail)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
