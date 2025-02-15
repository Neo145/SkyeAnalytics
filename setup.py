# F:\SkyeAnalytics\setup.py
from setuptools import setup, find_packages

setup(
    name="skye_analytics",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'sqlalchemy',
        'psycopg2-binary',
        'python-dotenv',
    ],
)