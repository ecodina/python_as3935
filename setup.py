from distutils.core import setup

setup(
  name='as3935',
  packages=['as3935'],
  version='0.1',
  license='gpl-3.0',
  description='A Python3 module to control the lightning detector AS3935 chip',
  author = 'Eloi Codina',
  author_email = 'eloi.codina@gmail.com',
  url = 'https://github.com/ecodina/python_as3935',
  download_url = 'https://github.com/ecodina/python_as3935/v_01.tar.gz',    # I explain this later on
  keywords = ['python', 'raspberry', 'gpio', 'lightning', 'sensor'],
  install_requires=[            # I get to this in a second
          'validators',
          'beautifulsoup4',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GNU General Public License v3.0',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7'
  ],
)