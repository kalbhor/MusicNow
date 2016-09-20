from setuptools import setup

setup(name='fluorine',
      version='0.2',
      description='Lets you download music with album art and details',
      url='https://github.com/lakshaykalbhor/Download-Music',
      author='Lakshay Kalbhor',
      author_email='lakshaykalbhor@gmail.com',
      license='MIT',
      packages =['fluorine'],
      install_requires=[
          'youtube-dl',
          'bs4',
          'mutagen',
          'requests'
      ],
      entry_points={
        'console_scripts': ['fluorine=fluorine.command_line:main'],
      },
      
      zip_safe=False
      )