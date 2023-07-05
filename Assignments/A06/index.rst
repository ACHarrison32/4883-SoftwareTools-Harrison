
A06 - Sphinx Presentation
===============================================
Sphinx is a widely used open-source documentation generation tool. It is commonly used to create documentation for software projects, libraries, and APIs. Sphinx supports various programming languages, but it is particularly popular in the Python community.

Downloading Sphinx
------------------
.. raw:: html

   <iframe width="560" height="315" src="https://www.youtube.com/embed/WcUhGT4rs5o" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

.. raw:: html

   <iframe width="560" height="315" src="https://www.youtube.com/embed/b4iFyrLQQh4" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

* Start by making sure you have **Python** downloaded. Check this with: *python - -version*
* Create a folder to keep all your Sphinx stuff in.
* You can then run the following command to install Sphinx: *pip install sphinx*

Running Sphinx
--------------
* Once Sphinx is installed run it by using the command: *sphinx-quickstart*

.. image:: /images/Sphinx_Quickstart.PNG

* This creates you Sphinx project now you create your HTML documents and document you python code.

Adding Extensions and Python Module Search Path
-----------------------------------------------
* First add your Python code documents in the folder that you quickstarted Sphinx in.
* Open up your conf.py file: *code conf.py*
* Add the following 3 lines to the file:

.. image:: /images/Sphinx_Python_Path.PNG

* Adding these 3 lines allows Sphinx to locate and import your project's modules during the documentation generation process
* Now we need to add the following Extensions:

.. image:: /images/Sphinx_Extensions.PNG

* *sphinx.ext.autodoc*: This extension is used to automatically generate API documentation from your Python code.
* *sphinx.ext.viewcode*: This extension adds links to the source code of documented Python objects, allowing users to easily view the source code.
* *sphinx.ext.napoleon*: This extension allows you to use Google-style or NumPy-style docstrings, providing support for more expressive and readable docstrings.
   
* Once you have added these extensions and the python path install the following command: *pip install sphinx-autodoc-typehints*
* You have now installed everything you need to document your python code

Creating Your rst Files and Including Modules
---------------------------------------------
* Now you want to make your rst files from your python code files.
* To do this run the following command: sphinx-apidoc -o <output_directory> <source_directory>

.. image:: /images/Sphinx_apidoc.PNG

* Once you have created the rst files, open your modules.rst file and make sure the follwing python file is called.

.. image:: /images/Sphinx_Modules.PNG

Making Your index.rst and Toctree's
-----------------------------------
* Toctree's are your Table of Contents Tree's 
* This is where you will add your modules.rst file that calls your specified modules
* You can add many toctree's and have them link to different files
* Create you index.rst using restructured text. This will be how your HTML cite looks.

.. toctree::
   :maxdepth: 2

   modules


