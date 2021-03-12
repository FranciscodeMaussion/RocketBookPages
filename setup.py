from setuptools import setup

setup(
    name='rocketqr',
    version='0.1',
    py_modules=['rocketqr', 'templates', 'constants'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        rocketqr=rocketqr:set_up
    ''',
)
