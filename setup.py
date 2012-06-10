"""
Flask-MailErrors
----------------

Simplifies setup of sending emails on errors in Flask application.
Uses Flask-Mail extension under the hood.
"""
from setuptools import setup


setup(
    name='Flask-MailErrors',
    version='1.0',
    url='http://github.com/flask-mailerrors/',
    license='BSD',
    author='Sergey Panfilov',
    author_email='sergray@gmail.com',
    description='Sends emails with errors in Flask application',
    long_description=__doc__,
    py_modules=['flask_mailerrors'],
    platforms='any',
    install_requires=[
        'Flask>=0.8',
        'Flask-Mail'
    ],
    test_suite='tests',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
