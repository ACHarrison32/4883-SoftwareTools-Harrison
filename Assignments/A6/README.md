# :computer: A06 - Sphinx
## :name_badge: Andrew Harrison
## :school: 4883 Software Tools
## :date: 06/25/2023

### :memo: Description
#### [Sphinx](https://www.sphinx-doc.org/en/master/) is a widely used open-source documentation generation tool. It is commonly used to create documentation for software projects, libraries, and APIs. Sphinx supports various programming languages, but it is particularly popular in the Python community.


## :computer: How To Install Sphinx:
#### Video link on how to install [Sphinx](https://www.youtube.com/watch?v=WcUhGT4rs5o)
#### Directions for installing [Sphinx](https://www.sphinx-doc.org/en/master/usage/installation.html)
#### Start by making sure you have [Python](https://www.python.org/downloads/release/python-3114/) downloaded. You can check this in the Command Terminal using: python --version
#### Create a folder to keep all your sphinx stuff in
#### Install sphinx: pip install sphinx

## :desktop_computer: Starting Sphinx:
#### Quickstart sphinx in command terminal: sphinx-quickstart
#### Fill out the next few questions:
<img src = "https://github.com/ACHarrison32/4883-SoftwareTools-Harrison/blob/main/Assignments/A6/images/Sphinx_Quickstart.PNG" >

#### This creates you Sphinx project now you create your HTML documents and document you python code.

## :electric_plug: Adding Extensions and Python Module Search Path
#### First add your Python code documents in the folder that you quickstarted Sphinx in.
#### Open up your conf.py file: code conf.py
#### Add the following 3 lines to the file:
<img src = "https://github.com/ACHarrison32/4883-SoftwareTools-Harrison/blob/main/Assignments/A6/images/Sphinx_Python_Path.PNG">

#### Adding these 3 lines allows Sphinx to locate and import your project’s modules during the documentation generation process
#### Now we need to add the following Extensions:
<img src = "https://github.com/ACHarrison32/4883-SoftwareTools-Harrison/blob/main/Assignments/A6/images/Sphinx_Extensions.PNG" >

#### sphinx.ext.autodoc: This extension is used to automatically generate API documentation from your Python code.
#### sphinx.ext.viewcode: This extension adds links to the source code of documented Python objects, allowing users to easily view the source code.
#### sphinx.ext.napoleon: This extension allows you to use Google-style or NumPy-style docstrings, providing support for more expressive and readable docstrings.
#### Once you have added these extensions and the python path install the following command: pip install sphinx-autodoc-typehints
#### You have now installed everything you need to document your python code

## :file_folder: Creating Your rst Files and Including Modules
#### Now you want to make your rst files from your python code files.
#### To do this run the following command: sphinx-apidoc -o <output_directory> <source_directory>
<img src = "https://github.com/ACHarrison32/4883-SoftwareTools-Harrison/blob/main/Assignments/A6/images/Sphinx_apidoc.PNG" >

#### Once you have created the rst files, open your modules.rst file and make sure the follwing python file is called.
<img src = "https://github.com/ACHarrison32/4883-SoftwareTools-Harrison/blob/main/Assignments/A6/images/Sphinx_Modules.PNG" >

## :bookmark_tabs: Making Your index.rst and Toctree’s
#### Toctree’s are your Table of Contents Tree’s
#### This is where you will add your modules.rst file that calls your specified modules
#### You can add many toctree’s and have them link to different files
#### Create you index.rst using restructured text. This will be how your HTML cite looks.

