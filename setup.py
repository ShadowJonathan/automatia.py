from setuptools import setup, find_packages

version = '0.2.2'

print(find_packages())

setup(
    name='automatia',
    packages=find_packages(),
    version=version,
    description='CLI swiss knife for all kinds of archive sites',
    author='Jonathan de Jong',
    author_email='jonathandejong02@gmail.com',
    url='https://github.com/ShadowJonathan/automatia.py',
    # download_url='https://github.com/ShadowJonathan/automatia.py/archive/{}.tar.gz'.format(version),
    # keywords=['testing', 'logging', 'example'],  # arbitrary keywords
    # classifiers=[],
    license="MIT",
    requires=['six'],
    python_requires='>=2.7',

    entry_points={
        'console_scripts': ['automatia=automatia.cli:main'],
    },
)
