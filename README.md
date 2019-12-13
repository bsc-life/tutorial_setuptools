# Instructions to build a command line application

- **Programming Language**: Python 3.6
- **Author**: Victoria Ruiz-Serra
- **e-mail**: victoria.ruizserra@bsc.es

*Note: This is a tutorial from an ammateur developer of a Python package. Despite my inexperience, I decided to share my little knwoledge and perhaps save some of your time. Since I struggled sometimes to understand and implement some of the functions of my command line app, I tried to point out those not-so-obvious steps. Theregore, I think this is a good manual if you are a beginner like me.*

**Here you will find an easy-to-follow recipe to build your own Python command-line application.**

-------------
## 1. Directory Structure

The directory structure, so far, should look like this:

```hl_lines="4" 
mypackage
|___ README
|___ MANIFEST.in
|___ setup.py
|___ application1
|          |___   __init__.py
|          |___   __main__.py 
|          |___   fun1.py
|          |___   ...
|          |___   data
|          |	    |___  data.dat
|          |	    |___  ...
|          |___   dependencies
|         	       |___  _dependencies.txt
|___ application2
           |___   __init__.py
           |___   __main__.py 
           |___   fun2.py
           |___   ...
```

Note: watch out!  write correctly the name of the scripts without any space in the case of `__main__.py`  and `__init__.py`

--------
## 2. Scripts content 

- `__init__.py`  → Usually is left empty

- `__main__.py` → Executes the command line app

```python 
# coding: utf-8
#"""mypackage.__main__: executed when mypackage directory is called as script."""
from .fun1 import main
if __name__ == '__main__':
   main()
```

- `fun1.py`
```python 
# coding: utf-8
def main():
   print('this is just a test for app1')
```

- `fun2.py`

```python 
# coding: utf-8
def main():
   print('this is just a test for app2')
```


- `dependencies.txt` contains the necessary Python dependencies of our package. This file can be obtained by executing:
```
pip freeze > dependencies.txt
```


- `data.dat` and `MANIFEST.in` are the file that contain the necessary data for the package and the file that tells the package to include this data respectively. An example of `MANIFEST.in`:

```
include data/data.dat
```

----
## 3. Setup of virtual environment

To test your package in 'developent mode' (i.e.: locally), we create a virtual environment. In this way, we avoid to install the package in our global library allowing us to correct possible mistakes more easily. 

To setup the virtual environment, we do the following: 


```shell
virtualenv -p python3 venv  # venv is created and contains the virtual environment 
. venv/bin/activate  #activate the environment
```
If everything went right, now, instead of
```shell
 $
```
 we have 

```shell
(venv) $
```
Anything we write from now on in our terminal will be executed **only** in the virtual environment that we have just created. 


----
## 4. Create setup.py 

An example of a `setup.py` script can be found [here](https://github.com/pypa/sampleproject/blob/master/setup.py) and the docummentation can be found [here](https://setuptools.readthedocs.io/en/latest/setuptools.html). Therefore, I will not extend on the concept of setup.py or which type of elements we can include. Hereby find an example of my [setup.py](https://github.com/bsc-life/tutorial_setuptools/blob/master/setup.py)

**Important info regarding package directory**: do not mistake `package_dir` with `package`. It is better to use only the variable `package` and this indicates the directory of our package!!! (really, it isn’t so obvious).

```python
# Always prefer setuptools over distutils 
from setuptools import setup, find_packages  # pylint: disable=no-name-in-module,import-error 
import io 
from os import path 
 
here = path.abspath(path.dirname(__file__)) 

# Get the long description from the README file 
with open(path.join(here, 'README.md'), encoding='utf-8') as f: 
   long_description = f.read() 
# Get the requirements of the packages 
with open('application1/dependencies/dependencies.txt') as f: 
   requirements = f.read().splitlines() 
# Arguments marked as "Required" below must be included for upload to PyPI. 
# Fields marked as "Optional" may be commented out. 
setup( 
   name='mypackage',  # Required 
   version='0.1.0',  # Required 
   author='NAME',  # Optional 
   author_email='EMAIL',  # Optional 
   url="https://github.com/user/yourpackage",  # Optional 
   # Note: To download the package first you have to make it public and do a release 
   download_url='https://github.com/user/pkg/archive/v_01.tar.gz',  
   description='Ashort description here',  # Optional 
   long_description=long_description,  # Optional 
   long_description_content_type='text/markdown',  # Optional 
   keywords=["some", "keywords", "heaywords"],  #Optional 
   packages=['application1', 'application2',],  # Required!!!!! 
   python_requires='>=3, <4', # Optional  
   install_requires=requirements,  # Optional 
   entry_points={ 
       "console_scripts": ['application1=application1.__main__:main', 
                           'application2=application2.__main__:main']   
   }, 
)
```

### **4.1 Data files**

When our code depends on data files and we want to include them in the installation process we need to add the option `package_data`. 


```python
setup(...,
      # And include any *.dat files found in the 'data' subdirectory
      # of the 'mypackage' package, also:
      package_data={'mypackage/application1': ['data/*'] }
   }, ...
)
```


[Here](https://setuptools.readthedocs.io/en/latest/setuptools.html#including-data-files) you can find a more detailed example. Remember to include the MANIFEST.in file to specify the location of the data files. [Here](https://wiki.python.org/moin/Distutils/Tutorial) you can find an example of the file. 


### **4.2 What if my package has an external dependency written in C.**

If that is your case, there is a nice and easy workaround to download and compile your package during the installation process. Find below more information about this. 

- **From [distutils documentation](https://docs.python.org/3.6/library/distutils.html)**:
*The [distutils](https://docs.python.org/3/library/distutils.html#module-distutils) package provides support for building and installing additional modules into a Python installation. The new modules may be either 100%-pure Python, or may be extension modules written in C, or may be collections of Python packages which include modules coded in both Python and C.*
*Most Python users will _not_ want to use this module directly, but instead use the cross-version tools maintained by the Python Packaging Authority. In particular,[ setuptools](https://setuptools.readthedocs.io/en/latest/) is an enhanced alternative to[ distutils](https://docs.python.org/3/library/distutils.html#module-distutils).*

- See an example of how to implement distutils [here](https://stackoverflow.com/questions/1754966/how-can-i-run-a-makefile-in-setup-py/1763900#1763900) and [here](https://github.com/Mykrobe-tools/mykrobe/blob/master/setup.py).

My example, based on the previous ones, can be found below. In my case, my package depends on [BCFTools](https://samtools.github.io/bcftools/bcftools.html), hosted in [GitHub](https://github.com/samtools/bcftools). All I had to do is to implement the downloading a installation instructions within my installation process. What I am doing is the next: 

   1) Tell setup.py to clone the necessary repositories.
   2) Compile the package
   3) Copy the necessary executable files to the bin directory


```python
#import disutils functionality already built in setuptools
from setuptools.command.install import install as DistutilsInstall

class git_clone_external(DistutilsInstall):

   def run(self):
       bcftools_dir = os.path.dirname(os.path.realpath(__file__)) + "bcftools"
       htslib_dir = os.path.dirname(os.path.realpath(__file__))+" htslib"

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
           ["cp", "bcftools", "%s/bin/" % os.environ.get('VIRTUAL_ENV', '/usr/local/')],
           cwd=bcftools_dir) 
       subprocess.call(
           ["cp", "plugins/split-vep.so", "%s/bin/" % os.environ.get('VIRTUAL_ENV', '/usr/local/')],
            cwd=bcftools_dir)

       DistutilsInstall.run(self)

...

setup(..., cmdclass={'install': git_clone_external}, ...)
```

Note: if you have written a dependency in C, then you should check the use of **`ext_modules`** in setup.py. 

----
## 5. Install the package

cd to your package directory and execute:

```shell 
pip install .     	
```

If you still want to add some changes and avoid doing `pip install . ` every time you add them, then execute:

```shell 
pip install -e .
```
This is the developer mode, so any change included in your code will be automatically updated in the code installed by pip.

**Note:** take into accound that this last command will not compile the dependencies and when executing the package, it will not work. 


### **Check if installation was succesful**

To check if the installation is well done, type: 

```shell
 pip show -f mypackage
```

The printed output should show the tree file structure indicated at the beginning of the tutorial copied in the `/bin` folder. 

Also, execute your command line application. 

```
 mypackage
```
Now your package should be executed correctly. 

---
## 6. Deactivate the virtual environment

After checking that the package works as expected, we deactivate and erase the virtual environment:  

```shell
deactivate
rm -r  venv_test_package
```

Now you are ready to distribute your package and install it outside of a virtual environment. 

---
## 7.Different ways to do the definitive installation of your package

### From GitHub

#### Clone and install the package

To install Python package from github, you need to clone that repository.

```shell
git clone https://github.com/suer/mypackage.git
```

Then just run the `setup.py` file from that directory,

```shell
sudo python setup.py install
```


#### PIP from public GitHub repository 

If the package is in a public repo, use either: 
```shell
pip install git+https://github.com/user/mypackage.git
```
or

```shell
pip install git+git://github.com/user/mypackage.git
```

#### PIP from private GitHub repository

If the project is hosted in a private repo, a ssh key needs to be generated. This allows permision to your computer to install the package. More details can be found [here](https://jdblischak.github.io/2014-09-18-chicago/novice/git/05-sshkeys.html). After this, the following command should run just fine: 

```
pip install git+ssh://git@github.com/user/mypackage.git
```

### From PiPy
This is the easiest and fastest way to install your package. 

```shell
pip install mypackage
```
To do this, the package should be published in PyPi. 
#### Note: How to upload my package to PyPi

Once your pacakge or application is ready, you can consider to upload it to PyPi. In this way, you will be able to install it. All details can be found [here](https://medium.com/@joel.barmettler/how-to-upload-your-python-package-to-pypi-65edc5fe9c56).


<!-- Docs to Markdown version 1.0β17 -->
