from distutils.core import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
  name='as3935',
  packages=['as3935'],
  version='0.1.4',
  license='gpl-3.0',
  description="A Python3 module to control the lightning detector AS3935 chip",
  long_description=long_description,
  long_description_content_type="text/x-rst",
  author = 'Eloi Codina',
  author_email = 'eloi.codina@gmail.com',
  url = 'https://github.com/ecodina/python_as3935',
  download_url='https://github.com/ecodina/python_as3935/archive/v0.1.4-beta.tar.gz',
  keywords = ['python', 'raspberry', 'gpio', 'lightning', 'sensor'],
  install_requires=[
          'pigpio',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7'
  ],
)
