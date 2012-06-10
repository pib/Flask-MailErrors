import unittest

from flask import Flask
from flask.ext import mailerrors

from mock import patch


class MailErrorsTests(unittest.TestCase):

    def setUp(self):
        app = Flask(__name__)

        @app.route('/error')
        def explicit_logger_error():
            app.logger.error('Error Message')
            return ''

        @app.route('/exception')
        def raise_unhandled_exception():
            """Should implicitly cause app logger.error call"""
            raise Exception('Exceptional Message')

        self.app = app
        self.test_client = app.test_client()

    @patch.object(mailerrors.Mail, 'send')
    def test_without_admins(self, mocked_send):
        mailerrors.init_app(self.app)
        self.app.logger.error('test without ADMINS')
        self.assertFalse(mocked_send.called)

    @patch.object(mailerrors.Mail, 'send')
    def test_with_admins(self, mocked_send):
        self.app.config['ADMINS'] = [
            ('Admin', 'admin@example.net'),
        ]
        mailerrors.init_app(self.app)
        self.test_client.get('/error')
        self.assertEqual(mocked_send.call_count, 1)
        msg = mocked_send.call_args[0][0]
        self.assertEqual(msg.subject, 'Error in Flask app')
        self.assertTrue('Error Message' in msg.body)
        self.assertEqual(msg.recipients, ['admin@example.net'])
        self.test_client.get('/exception')
        self.assertEqual(mocked_send.call_count, 2)
        msg = mocked_send.call_args[0][0]
        self.assertTrue('Exceptional Message' in msg.body)

    def test_double_init(self):
        handlers_before_init = len(self.app.logger.handlers)
        mailerrors.init_app(self.app)
        mailerrors.init_app(self.app)
        handlers_after_init = len(self.app.logger.handlers)
        self.assertEqual(handlers_before_init + 1, handlers_after_init)


if __name__ == '__main__':
    unittest.main()
