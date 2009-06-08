from distutils.core import setup

long_description = '' #open('README.rst').read()

setup(
    name='django-simplesurvey',
    version="0.1",
    package_dir={'simplesurvey': 'simplesurvey'},
    packages=['simplesurvey'],
    description='Django simplesurvey',
    author='Jeremy Carbaugh',
    author_email='jcarbaugh@sunlightfoundation.com',
    license='BSD License',
    url='',
    long_description=long_description,
    platforms=["any"],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Environment :: Web Environment',
    ],
)
