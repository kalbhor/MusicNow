from setuptools import setup

setup(name='download-music',
      version='0.1',
      description='Lets you download music with album art and details',
      url='https://github.com/lakshaykalbhor/Music-Downloader',
      author='Lakshay Kalbhor',
      author_email='lakshaykalbhor@gmail.com',
      license='MIT',
      packages=['download-music'],
      scripts=["bin/download-music"],
      install_requires=[
          'youtube-dl',
          'bs4',
          'mutagen',
          'requests'
      ],
      zip_safe=False
      )