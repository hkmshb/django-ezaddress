import os
from setuptools import setup



version = '0.3'


setup(
    name='django-ezaddress',
    version=version,
    zip_safe=False,
    
    author='Abdul-Hakeem Shaibu',
    author_email='hkmshb@gmail.com',
    maintainer='Abdul-Hakeem Shaibu',
    maintainer_email='hkmshb@gmail.com',
    url='https://github.com/hkmshb/django-ezaddress',
    description='A django application for working with and handling addresses.',
    long_description=open(os.path.join(os.path.dirname(__file__), 
                                       'README.md')).read(),
    packages=['ezaddress'],
    test_suite='runtests.run_tests',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Framework :: Django 1.7',
        'Framework :: Django 1.8',
        'Intended Audience :: Developers',
        'License ::',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)