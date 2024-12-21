from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()


setup_args = dict(
    name='django-query-to-table',
    version='1.1.0',
    description='A simple to use Django package to turn your queryset and sql query into a beautiful reporting html table',
    long_description_content_type="text/markdown",
    long_description=README,
    license='GNU',
    packages=find_packages(),
    author='M.Shaeri',
    
    keywords=['Django', 'Report', 'HTML', 'Table', 'SQL'],
    url='https://github.com/birddevelper/django-query-to-table',
    download_url='https://pypi.org/project/django-query-to-table/'
)

install_requires = [
    'Django'
]

if __name__ == '__main__':
	setup(**setup_args, install_requires=install_requires)
