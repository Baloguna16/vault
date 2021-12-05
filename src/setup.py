from setuptools import setup

setup(
    name='no-secrets-here',
    version='1.0.0',
    py_modules=['no-secrets-here'],
    install_requires=[
        'pytz',
        'click',
        'datetime',
        'werkzeug',
        'cryptography'
    ],
    entry_points={
        'console_scripts': [
            'vault = vault.cli:interface',
        ],
    },
)
