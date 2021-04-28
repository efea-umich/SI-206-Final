# Isolating Satire with Machine Learning

## SI 206 Final Project

### By Efe Akinci and Michael Zhou

## Notes

In the interest of keeping file sizes small, we have not included the training data used to create the machine learning algroithm (~111MB).<br>
If you are interested in exploring the training data, you can find the dataset we used [here](https://www.kaggle.com/clmentbisaillon/fake-and-real-news-dataset/).

## Introduction

Onion articles (and other satirical articles) are pretty funny. Even though they are written like news, we can usually tell that they are meant to be satire. But, we wondered, could a computer do the same? We used Kaggle, Keras, Tensorflow, Pandas, and others to find out.

## "I don't have a the equipment to train the machine learning model."

You can find a link to our pre-trained weights [here](https://drive.google.com/file/d/16qm8NDTlUAE0heBX1GF2hRrfYoZuvsFO/view?usp=sharing) (link is currently restricted to U-M accounts).<br>
Warning: The file download is quite large at ~140 MB.

## More info

Our final project report includes more information on what this project does, how it works, and how it could be improved. It is included in our project as `Final_Project_Report.pdf`.

## Directions to Important Files

### **Getting Data**

**Our data collection file is `onion_farmer.py`**<br>

*API's/Websites Used: CNN, The Onion, AP News, Clickhole, Pushshift API (for Reddit).*<br>

**Data is stored in the database file `static\onion_barn.db`.**<br>

*To limit data points collected to 25 at a time, we scrape webpages one article at a time. For Pushshift API, we used a recursive call to ensure that we could get more than 25 articles at once without exceeding the 25/call limit.*

### **Processing Data**

**Averages, percentages, and more are calculated from the data in `visuals.py`.**<br>

*Our JOIN statement is used in `most_commented` on line 34 of `visuals.py`.*<br>

**The output from calculations is written to `static\caulculations.csv`.**<br>

### **Visualizations**

**Our visualizations are stored in `static\visuals`.**<br>

*We have also generated wordclouds from our training datasets, found in `static\visualizations`.*

### **Report**

**Our project report can be found at `Final_Project_Report.pdf`.**