from setuptools import setup, setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='wav2sfz',
    version='0.0.0',
    description='Convert Wave files to an SFZ soundfonts to play audio tracks in Musescore',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/paulchoisel/wav2sfz',
    author='Paul Choisel',
    author_email='paul.choisel@gmail.com',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Artistic Software',
        'Natural Language :: English',
        'Programming Language :: Python'
    ],

    keywords='musescore audio wav notation music score track',

    packages=setuptools.find_packages(),

    entry_points={
        'console_scripts': [
            'wav2sfz = wav2sfz.wav2sfz:main'
        ],
        'gui_scripts': [
            'wav2sfz-gui = wav2sfz.gui:main'
        ]
    },

    install_requires=[
        'pygubu',
        'pymusicxml'
    ],

    package_data={
        'ui': ['UI/ui.ui'],
        'yaru': ['UI/yaru/*'],
        'favicon': ['UI/favicon.png']
    }
)
