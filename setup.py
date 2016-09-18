from setuptools import setup

setup(name='musicdownload',
      version='0.1',
      description='Lets you download music with album art and details',
      url='https://github.com/lakshaykalbhor/Music-Downloader',
      author='Lakshay Kalbhor',
      author_email='lakshaykalbhor@gmail.com',
      license='MIT',
      packages=['musicdownload'],
      install_requires=[
          'youtube-dl',
          'bs4',
          'mutagen',
          'requests'
      ],
      zip_safe=False
      )