# Isolating Satire with Machine Learning

## SI 206 Final Project

### By Efe Akinci and Michael Zhou

## Notes

In the interest of keeping file sizes small, we have not included the training data used to create the machine learning algroithm (~111MB).
If you are interested in exploring the training data, you can find the dataset we used [here](https://www.kaggle.com/clmentbisaillon/fake-and-real-news-dataset/).

## Introduction

For humans, it's quite simple to see whether an article is satirical or not by reading through it.

We wondered: Could we train a Machine to do the same?

## Methodology

First, we pulled real and fake news articles and their headlines from a publicly available database on Kaggle. [linked here](https://www.kaggle.com/clmentbisaillon/fake-and-real-news-dataset/)

## Setting Up Your Own Virtual Environment

Install the VirtualEnv package.

`py -m pip install virtualenv`

Next, create a folder for the virtual environment.

`py -m virtualenv venv`

Activating your virtual environment:

`.\\venv\Scripts\activate #for Windows`

We have written a list of package/library requirements for the project in requirements.txt.

Download all necessary packages to run this project:

`py -m pip install -r requirements.txt`

To exit:

`deactivate`
