# Instructions to build a command line application

**Programming Language**: Python 3.6
**Author**: Victoria Ruiz-Serra
**e-mail**: victoria.ruizserra@bsc.es

*Note: This is a tutorial from an ammateur developer of a Python package. Despite my inexperience, I decided to share my little knwoledge and perhaps save some of your time. Since I struggled sometimes to understand and implement some of the functions of my command line, I tried to point out those not-so-obvious steps. I think this is a good manual if you are a beginner like me.*

**Here you will find an easy-to-follow recipe to build your own Python command-line application.**


# DIRECTORY STRUCTURE

The directory structure, so far, should look like this:

**mypackage**

|___ _ README_

|___ _ MANIFEST.in_

|___ _ setup.py_

|___ **application1**

|          |___   ___init__.py_

|          |___   ___main__.py _ watch out!  write correctly the name of the scripts without any space

|          |___   _fun1.py_

|          |___   …

|          |___   data

|          |	       |___  _data.dat_

|          |___   dependencies

|         	       |___  _dependencies.txt_

|___ **application2**

           |___   ___init__.py_

           |___   ___main__.py _ 

           |___   _fun2.py_

           |___   …


# SCRIPTS 

__init__.py  → Usually is left empty

__main__.py → Executes the command line app


```
# coding: utf-8
#"""mypackage.__main__: executed when mypackage directory is called as script."""
from .fun1 import main
if __name__ == '__main__':
   main()
```


fun1.py


```
# coding: utf-8
def main():
   print('this is just a test for app1')
```


fun2.py


```
# coding: utf-8
def main():
   print('this is just a test for app2')
```


dependencies.txt

data.dat and MANIFEST.in


# 1 - SETUP OF VIRTUAL ENVIRONMENT

To test your package locally, first we create a virtual environment. In this way, we avoid to install the package in our library when it is in “developer” or unfinished mode. To setup the virtual environment, we do the following: 


```
virtualenv -p python3 venv
. venv/bin/activate
```


Now, instead of $ in the terminal, we have: 


```
(venv) $
```


Anything we write from now on in our terminal will be executed **only** in the virtual environment that we have created. 


# 2 - CREATE setup.py 

An example of a setup.py script can be found [here](https://github.com/pypa/sampleproject/blob/master/setup.py) and [here](https://setuptools.readthedocs.io/en/latest/setuptools.html).

Important info regarding package directory: do not mistake `package_dir `with` package. `It is better to use only the variable` package `and this should indicate the directory of our package!!! (really, it isn’t so obvious).


<table>
  <tr>
   <td><code># Always prefer setuptools over distutils \
from setuptools import setup, find_packages  # pylint: disable=no-name-in-module,import-error \
import io \
from os import path \
 \
here = path.abspath(path.dirname(__file__)) \
# Get the long description from the README file \
with open(path.join(here, 'README.md'), encoding='utf-8') as f: \
   long_description = f.read() \
# Get the requirements of the packages \
with open('mypackage/dependencies/dependencies.txt') as f: \
   requirements = f.read().splitlines() \
# Arguments marked as "Required" below must be included for upload to PyPI. \
# Fields marked as "Optional" may be commented out. \
setup( \
   name='mypackage',  # Required \
   version='0.1.0',  # Required \
   author='Victoria Ruiz-Serra',  # Optional \
   author_email='',  # Optional \
   url="https://github.com/user/yourpackage",  # Optional \
   # NOTE!: To download the package first you have to make it public and do a release \
   download_url='https://github.com/user/yourpackage/archive/v_01.tar.gz',  \
   description='Ashort description here',  # Optional \
   long_description=long_description,  # Optional \
   long_description_content_type='text/markdown',  # Optional (see note above) \
   keywords=["some", "keywords", "heaywords"],  #Optional \
   packages=['application1', 'application2',],  # Required!!!!! \
   python_requires='>=3, <4', # Optional  \
   install_requires=requirements,  # Optional \
   entry_points={ \
       "console_scripts": ['application1=application1.__main__:main', \
                           'application2=application2.__main__:main']   \
   }, \
)</code>
   </td>
  </tr>
  <tr>
   <td>
   </td>
  </tr>
</table>



# 


# Including data files

When our code depends on data files and we want to include this in the installation we need to add the option ‘package data’ in our setup.py. 


```
   package_data={
       # And include any *.dat files found in the 'data' subdirectory
       # of the 'mypkg' package, also:
       'pdbmapper': ['data/*']
   },
```


[Here](https://setuptools.readthedocs.io/en/latest/setuptools.html#including-data-files) you can find a more detailed explanation. Remember to include a MANIFEST.in file to specify the location of the data files. [Here](https://wiki.python.org/moin/Distutils/Tutorial) you can find an example of that file. 


# My package has c++ dependencies

The[ distutils](https://docs.python.org/3/library/distutils.html#module-distutils) package provides support for building and installing additional modules into a Python installation. The new modules may be either 100%-pure Python, or may be extension modules written in C, or may be collections of Python packages which include modules coded in both Python and C.

Most Python users will _not_ want to use this module directly, but instead use the cross-version tools maintained by the Python Packaging Authority. In particular,[ setuptools](https://setuptools.readthedocs.io/en/latest/) is an enhanced alternative to[ distutils](https://docs.python.org/3/library/distutils.html#module-distutils) that provides:

See an example of how to implement distutils  [here](https://stackoverflow.com/questions/1754966/how-can-i-run-a-makefile-in-setup-py/1763900#1763900) and [here](https://github.com/Mykrobe-tools/mykrobe/blob/master/setup.py).

My example can be found below. My package depends on BCFTools which is hosted in github. I just indicate the download 


```
#import disutils functionality already built in setuptools
from setuptools.command.install import install as DistutilsInstall

class git_clone_external(DistutilsInstall):
   def run(self):

       bcftools_dir = os.path.dirname(os.path.realpath(__file__)) + "/bcftools"
       htslib_dir = os.path.dirname(os.path.realpath(__file__))+" /htslib"

       if not os.path.exists(htslib_dir):
           command1 = ['git', 'clone', 'git://github.com/samtools/htslib.git', ]
           subprocess.call(command1, cwd=os.path.dirname(os.path.realpath(__file__)))

       if not os.path.exists(path.join(bcftools_dir, 'bcftools')):
           command2 = ['git', 'clone', 'git://github.com/samtools/bcftools.git']
           subprocess.call(command2, cwd=os.path.dirname(os.path.realpath(__file__)))
       subprocess.call(["make", "clean"], cwd=bcftools_dir)
       subprocess.call(['make'], cwd=bcftools_dir)
      # With the following line we cp the necessary compiled scripts used by my
      # program. You have to figure out where to find this scripts. Take into account
      # that my working dir is 'bcftools_dir'. 
       subprocess.call(
           ["cp", "bcftools", "%s/bin/" % os.environ.get('VIRTUAL_ENV', '/usr/local/')], cwd=bcftools_dir) 
       subprocess.call(
           ["cp", "plugins/split-vep.so", "%s/bin/" % os.environ.get('VIRTUAL_ENV', '/usr/local/')], cwd=bcftools_dir)

       DistutilsInstall.run(self)

...

setup(..., cmdclass={'install': MyInstall}, ...)
```


Note: if you have written a dependency in C, then you should check the use of **‘ext_modules’ **in setup.py. 


# 3.A - INSTALL THE PACKAGE

cd to your package directory and the execute:


```
pip install .     	
```


If you still want to add some changes and avoid doing `pip install . `every time you add some changes, execute :


```
pip install -e .
```


This is the developer mode, so any change included in your code will be automatically updated in the code installed by pip.

To check if the installation is well done, type: 


```
pip show -f mypackage
```


In the printed output you should see the tree structure indicated at the beginning of the tutorial  but this time is stored in the /bin folder. 


# How to install a PIP package hosted on a public or private Github repository

If the package is in a public repo,you need to use the proper git URL. Use: 


```
pip install git+https://github.com/vicruiser/PDBmapper.git
```


or


```
pip install git+git://github.com/vicruiser/PDBmapper.git
```


 If the project is hosted in a private repo, more details can be found [here](https://dev.to/rf_schubert/how-to-create-a-pip-package-and-host-on-private-github-repo-58pa). The following command should run just fine: 


```
pip install git+ssh://git@github.com/vicruiser/PDBmapper.git
```


3.B HOW TO UPLOAD MY PACKAGE TO PyPi

All details can be found [here](https://medium.com/@joel.barmettler/how-to-upload-your-python-package-to-pypi-65edc5fe9c56). 

4 - EXECUTE COMMAND-LINE APPLICATION

Now, by just typing ‘mypackage’ in the command line , the package should be executed.

5 - CLOSE THE VIRTUAL ENVIRONMENT

After checking that the package works as expected, we deactivate and erase the virtual environment:  


```
deactivate
rm -r  venv_test_package
```


Now you are ready to distribute your package and install it outside of a virtual environment. 


<!-- Docs to Markdown version 1.0β17 -->
