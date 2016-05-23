from setuptools import setup

setup(
    name='lektor-google-drive',
    version='0.1',
    author='David Baumgold',
    author_email='david@davidbaumgold.com',
    license='MIT',
    py_modules=['lektor_google_drive'],
    entry_points={
        'lektor.plugins': [
            'google-drive = lektor_google_drive:GoogleDrivePlugin',
        ]
    },
    install_requires=['requests'],
)
