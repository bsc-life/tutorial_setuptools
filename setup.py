# Always prefer setuptools over distutils
from setuptools import setup, find_packages  # pylint: disable=no-name-in-module,import-error
# import disutils functionality already built in setuptools
from setuptools.command.install import install as DistutilsInstall
import io
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
# Get the requirements of the packages
with open('mypackage/dependencies/dependencies.txt') as f:
    requirements = f.read().splitlines()

# external repository in C


class git_clone_external(DistutilsInstall):
    def run(self):

        bcftools_dir = os.path.dirname(
            os.path.realpath(__file__)) + "/bcftools"
        htslib_dir = os.path.dirname(os.path.realpath(__file__))+" /htslib"

        if not os.path.exists(htslib_dir):
            command1 = ['git', 'clone',
                        'git://github.com/samtools/htslib.git', ]
            subprocess.call(command1, cwd=os.path.dirname(
                os.path.realpath(__file__)))

        if not os.path.exists(path.join(bcftools_dir, 'bcftools')):
            command2 = ['git', 'clone',
                        'git://github.com/samtools/bcftools.git']
            subprocess.call(command2, cwd=os.path.dirname(
                os.path.realpath(__file__)))
        subprocess.call(["make", "clean"], cwd=bcftools_dir)
        subprocess.call(['make'], cwd=bcftools_dir)
        subprocess.call(
            ["cp", "bcftools", "%s/bin/" % os.environ.get('VIRTUAL_ENV', '/usr/local/')], cwd=bcftools_dir)
        subprocess.call(
            ["cp", "plugins/split-vep.so", "%s/bin/" % os.environ.get('VIRTUAL_ENV', '/usr/local/')], cwd=bcftools_dir)

        DistutilsInstall.run(self)


# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.
setup(
    name='mypackage',  # Required
    version='0.1.0',  # Required
    author='Victoria Ruiz-Serra',  # Optional
    author_email='',  # Optional
    url="https://github.com/user/yourpackage",  # Optional
    # Note: To download the package first you have to make it public and do a release
    download_url='https://github.com/user/pkg/archive/v_01.tar.gz',
    description='Ashort description here',  # Optional
    long_description=long_description,  # Optional
    long_description_content_type='text/markdown',  # Optional
    keywords=["some", "keywords", "heaywords"],  # Optional
    packages=['application1', 'application2', ],  # Required!!!!!
    python_requires='>=3, <4',  # Optional
    install_requires=requirements,  # Optional
    entry_points={
        "console_scripts": ['application1=application1.__main__:main',
                            'application2=application2.__main__:main']
    },
    package_data={'pdbmapper': ['data/*']},
)
