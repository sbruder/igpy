import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='igpy',
    version='0.0.1',
    author='Simon Bruder',
    author_email='dev+igpy@sbruder.de',
    description='igpy is a simple object-oriented API for instagram using the end-user GraphQL API.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/sbruder/igpy',
    packages=setuptools.find_packages(),
    install_requires=[
        'requests',
        'progressbar2'
    ],
    classifiers=(
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ),
)
