!/usr/bin/env python

from distutils.core import setup

setup(name='Distutils',
      version='2.1',
      description='DLBot - Python Discord Bot',
      author='Foxlider',
      author_email='foxlider.atom@gmail.com',
      url='https://github.com/Foxlider/DLBot-Discordbot',
      download_url='https://github.com/Foxlider/DLBot-Discordbot/archive/2.0.zip',
      Extension(libraries=['discord', 'asyncio', 'aiohttp', 'websockets', 'datetime', 'feedparser'])
      data_files=[('data', ['token.txt']),
                  ('logs', ['logs.txt']),
                  ('superlogs', ['superlogs.txt'])]
     )
