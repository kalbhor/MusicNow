from setuptools import setup

setup(name='musicnow',
      version='2.6',
      description='Lets you download music with album art and metadata',
      url='https://github.com/lakshaykalbhor/MusicNow',
      author='Lakshay Kalbhor',
      author_email='lakshaykalbhor@gmail.com',
      license='MIT',
      packages =['musicnow'],
      install_requires=[
          'youtube-dl',
          'bs4',
          'mutagen',
          'requests',
          'spotipy',
          'six',
          'colorama',
      ],
      entry_points={
        'console_scripts': ['musicnow=musicnow.command_line:main'],
      }
      )