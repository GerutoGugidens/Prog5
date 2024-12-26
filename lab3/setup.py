from setuptools import setup, find_packages

setup(name='p5l3_weatherdata_package',
      version='1.0',
      author="Geruto",
      author_email='gerutogugidens@gmail.com',
      description='A package for retrieving weather data using the OpenWeatherMap API.',
      packages=find_packages(),
      python_requires=">=3.6",
      install_requires=[
          "requests"
      ])