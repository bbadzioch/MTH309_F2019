# CDSE Days 2019
# Python Workshop


##  Workshop notebook files

Jupyter Notebook files used during this workshop are posted below. Each notebook
is posted as an ipynb file (which can be downloaded and opened in Jupyter Noptebook)
and as an html file (viewable online). I did not cover Notebook 3 during the workshop
due to lack of time.

* Notebook 1: Jupyter and Python Basics:  [ipynb](CDSE_Python_1_Intro.ipynb)  [html](CDSE_Python_1_Intro.html)

* Notebook 2: Web Scrapping with Pandas and BeautifulSoup: [ipynb](CDSE_Python_2_Soup.ipynb)  [html](CDSE_Python_2_Soup.html)

* Notebook 3: Computing with Numpy: [ipynb](CDSE_Python_3_Numpy.ipynb)  [html](CDSE_Python_3_Numpy.html)

* Notebook 4: Analyzing Data with Pandas: [ipynb](CDSE_Python_4_Pandas.ipynb)  [html](CDSE_Python_4_Pandas.html)

---


*Welcome to the Python workshop page.  Below you will find some informations about the workshop
and how to prepare for it. I am looking forward to meeting you on April 9.*

*Bernard Badzioch*


##  General information

* This will be a hands-on workshop - we will write and execute code the entire time.
All participants need to bring laptops. Any operating system (Windows/Mac/Linux) is fine.
Instructions how to install software and additional files we will use are posted below.

* I set up a [Piazza](http://piazza.com/buffalo/spring2019/cdsepython) page
for the workshop. Please sign up so you can post question before, during, and after
the workshop, or perhaps comment on questions posted by others.  


## Software installation

**1)** Install the [Anaconda distribution of Python 3.7](https://www.anaconda.com/download)
(be sure to select the 3.7 version).

If you have Anaconda previously installed, make sure that it includes Python 3.6
or 3.7, and fairly recent versions of the the Jupter Notebook and the following
Python packages: numpy, matplotlib, bokeh, pandas, requests, beautifulsoup4. Upgrade if needed.
If you are installing Anaconda for the first time, you don't need to worry about it, everything
is included in the distribution.  

**2)** A part of the Anaconda distribution is the Jupyter Notebook app.  It can be launched by typing:

```jupyter notebook```

in a terminal (Mac and Linux)  or command prompt (Windows). Once you execute
this command, a web browser will open showing Jupyter Notebook dashboard.  Here is a short
video which demonstrates basic functionality of the Jupyter Notebook (watching the first
4 minutes or so will be enough for now):

<div align="center">
<iframe  max-width="100%" width="560px" height="315px" src="https://www.youtube.com/embed/BJnro9jQ3fE" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>
<br/>

**3)** Launch Jupyter Notebook and open a new notebook. Copy the following code into an empty
notebook code cell:

```
import requests
r = requests.get("https://git.io/fhxxf").text
with open("cdse_resources.py", 'w') as f: f.write(r)
import cdse_resources
```

Execute the cell by pressing  `Shift-Enter` keys. The code will download a few files over the internet,
so you need to be connected to the network before you execute.

If everything goes fine, you will see a message saying that your computer is set up
for the workshop:

![Success](images/success.png)

If you run into difficulties please post a message on [Piazza](http://piazza.com/buffalo/spring2019/cdsepython).
