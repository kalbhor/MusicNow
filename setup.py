from setuptools import setup

setup(name='metamusic',
      version='0.1',
      description='Lets you download music with album art and details',
      url='https://github.com/lakshaykalbhor/Download-Music',
      author='Lakshay Kalbhor',
      author_email='lakshaykalbhor@gmail.com',
      license='MIT',
      packages =['metamusic'],
      install_requires=[
          'youtube-dl',
          'bs4',
          'mutagen',
          'requests'
      ],
      entry_points={
        'console_scripts': ['metamusic=metamusic.command_line:main'],
      },
      
      zip_safe=False
      )