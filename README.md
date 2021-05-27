# Assignment 1: Dictionary-Based Sentiment Analysis

### Description of Task <br>
This assignment was assigned by the course instructor as “Assignment 3 – Sentiment Analysis”. The purpose of the assignment was to utilize a dictionary-based sentiment analysis on a dataset consisting of over a million headlines from the Australian news source ABC from 2003 to 2020. This dataset is available on Kaggle  and provided in the repository. The assignment included calculating the sentiment score for every headline in the data using the spaCyTextBlob approach, a dictionary-based approach introduced during class. Furthermore, the task involved calculating and plotting rolling sentiment averages, and drawing inferences based on these plots about the sentiment scores of the headlines over time. 


### Content and Repository Structure <br>
If the user wishes to engage with the code and reproduce the obtained results, this section includes the necessary instructions to do so. It is important to remark that all the code that has been produced has only been tested in Linux and MacOS. Hence, for the sake of convenience, I recommend using a similar environment to avoid potential problems. 
The repository follows the overall structure presented below. The python sentiment.py script is located in the src folder. The data on which the sentiment analysis has been performed is provided in the data folder, and the outputs produced when running the script can be found within the output folder. The README file contains a detailed run-through of how to engage with the code and reproduce the contents.

| Folder | Description|
|--------|:-----------|
| ```data``` | A folder containing the data on which the sentiment analysis is performed.
| ```src``` | A folder containing the ```sentiment.py```script for the particular assignment.
| ```output``` | A folder containing the outputs produced when running the python scripts within the src folder.
| ```requirements.txt```| A file containing the dependencies necessary to run the python script.
| ```create_sentiment_venv.sh```| A bash-file that creates a virtual environment in which the necessary dependencies listed in the ```requirements.txt``` are installed. This script should be run from the command line.
| ```LICENSE``` | A file declaring the license type of the repository.


### Usage and Technicalities <br>
To reproduce the results of this assignment, the user will have to create their own version of the repository by cloning it from GitHub. This is done by executing the following from the command line: 

```
$ git clone https://github.com/sofieditmer/sentiment_analysis.git
```

Once the user has cloned the repository, a virtual environment must be set up in which the relevant dependencies can be installed. To set up the virtual environment and install the relevant dependencies, a bash-script is provided, which creates a virtual environment and installs the dependencies listed in the requirements.txt file when executed. To run the bash-script that sets up the virtual environment and installs the relevant dependencies, the user must first navigate to the sentiment_analysis repository:

```
$ cd sentiment_analysis
$ bash create_sentiment_venv.sh 
```

Once the virtual environment has been set up and the relevant dependencies listed in requirements.txt have been installed within it, the user is now able to run the sentiment.py script provided in the src folder directly from the command line. In order to run the script, the user must first activate the virtual environment in which the script can be run. Activating the virtual environment is done as follows:

```
$ source sentiment_venv/bin/activate
```

Once the virtual environment has been activated, the user is now able to run the sentiment.py script within it:

```
(sentiment_venv) $ cd src
(sentiment_venv) $ python sentiment.py
```

The user is able to modify the following parameters, however, this is not compulsory:

```
-i, --input_data: str <name-of-input-data >, default = "abcnews-date-text.csv"
-b, --batch_size: int <size-of-batches>, default = 500
-o, --output_filename: str <name-of-output-file>, default = "headlines_sentiment_scores.csv"
```

The abovementioned parameters allow the user to adjust the analysis of the input data, if necessary, but default parameters have been set making the script run without explicitly specifying these arguments. The user is able to modify the data on which to perform the sentiment analysis, the size of the batches to process at a time, as well as the name of the output CSV-file. 

### Output <br>
When running the ```sentiment.py```script, the following files will be saved in the ```output``` folder:
1. ```headlines_sentiment_scores.csv``` a dataframe showing the sentiment score for each headline.
2. ```smoothed_sentiment_7d_rolling_average.png``` a plot showing 1-week rolling sentiment average.  
3. ```smoothed_sentiment_30d_rolling_average.png``` a plot showing 1-month rolling sentiment average.
4. ```sentiment_barplot.png```barplot displaying the number of headlines for each sentiment category.

### Discussion of Results <br>
With both a 1-week and 1-month rolling average the sentiment scores of the news headlines generally lie above 0 indicating a very slight positive sentiment. Hence, it seems that most news headlines from this particular news station display a relatively neutral sentiment. With a 1-week rolling average the sentiment scores generally range between 0 and 0.05 (see figure 1). However, around 2006-2007 there is a significant decrease in sentiment scores. When assessing the sentiment scores with a 1-month rolling average, less variation is present (see figure 2). What is interesting is the slight increase in sentiment scores between 2012 and 2016, as well as the slight decrease in sentiment scores starting around 2005 and lasting to around 2010. One could suspect that this slight decrease in average sentiment might be due to the financial crisis that took place around this time.

<p float="center">
  <img src="https://github.com/sofieditmer/sentiment_analysis/blob/main/output/smoothed_sentiment_7d_rolling_average.png" width="400" height = "400" />
  <img src="https://github.com/sofieditmer/sentiment_analysis/blob/main/output/smoothed_sentiment_30d_rolling_average.png" width="400" height = "400" /> 
</p> 
Figure 1: Sentiment scores with 1-week and 1-month rolling averages. <br> <br>

To inform the plots displaying sentiment scores over time, I also produced a plot displaying the number of headlines for each sentiment category (see figure 2). When considering the three plots in relation to one another, it becomes clear that there is a general tendency of the news headlines being relatively neutral in sentiment. When only assessing the number of positive and negative news headlines in relation to one another, there are slightly more news headlines with a positive sentiment, which corresponds well to the tendency of the plots displaying sentiment scores over time. 
However, most news headlines seem to have a sentiment score of 0. This is most likely due to the vocabulary size of the dictionary used to estimate the sentiment scores of the news headlines. One could suspect that the headlines with an estimated sentiment score of 0 is most likely due to the fact that they contain words that are not present in the sentiment dictionary. Hence, when a word is not within the dictionary it is automatically assigned a value of 0 which explains why the vast majority of news headlines are categorized as “neutral”. This aspect also demonstrates a more general problem with the dictionary-based approach to sentiment analysis; that dictionary-based sentiment analyses are only able to handle words that are present in the dictionary.

<img src="https://github.com/sofieditmer/sentiment_analysis/blob/main/output/sentiment_barplot.png" width="500">
Figure 2: Number of news headlines in each sentiment category. <br> <br>

When examining the documentation of the spaCyTextBlob  and the dictionary used to estimate the sentiment scores, it becomes clear that the vast majority of annotated words are adjectives. While the primary use of adjectives for sentiment analysis makes perfect sense, given that adjectives are most commonly used to express sentiment, it also means that other word classes that carry valence and an inherent sentiment are not evaluated, which demonstrates another problem with the dictionary-based approach to sentiment analysis. 
To overcome the limitations of employing a dictionary-based approach to sentiment analysis, one could instead have employed a machine learning approach or even a deep learning approach, in which a model learns the relationship between linguistic features in the text and their sentiment, and can then be used to classify new, unseen texts. This kind of method could potentially improve the results obtained by a dictionary-based approach. 
