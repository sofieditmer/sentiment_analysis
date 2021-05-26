#!/usr/bin/env python
"""
Info: This script calculates the sentiment score for every headline in the abcnews-date-text.csv dataset which consists of over 1 million news headlines published over a period of 18 years. A plot of sentiment scores over time with a 1-week rolling average and a 1-month rolling average are created and saved to the output directory. Both plots have clear values on the x-axis, x- and y-labels, and a title.

Parameters:
    (optional) input_data: str <name-of-data>, default = "abcnews-date-text.csv"
    (optional) batch_size: int <size-of-batches>, default = 500
    (optional) output_filename: str <name-of-output-file>, default = "headlines_sentiment_scores.csv"

Usage:
    $ python sentiment.py
    
Output:
    - headlines_sentiment_scores.csv: a dataframe showing the sentiment score for each headline.
    - smoothed_sentiment_7d_rolling_average.png: a plot showing 1-week rolling sentiment average.  
    - smoothed_sentiment_30d_rolling_average.png: a plot showing 1-month rolling sentiment average.
    - sentiment_barplot.png: barplot displaying the number of headlines for each sentiment category.
"""

### DEPENDENCIES ###

# Core libraries
import os 
import sys
sys.path.append(os.path.join(".."))

# Pandas, matplotlib, numpy, seaborn
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# SpaCy
import spacy
from spacytextblob.spacytextblob import SpacyTextBlob
nlp = spacy.load('en_core_web_sm') # Initialize spaCy by creating a spaCy object
spacytextblob = SpacyTextBlob() # Initialize SpacyTextBlob
nlp.add_pipe(spacytextblob) # add spacytextblob to the pipeline

# argparse
import argparse

### MAIN FUNCTION ### 

def main():
    
    ### ARGPARSE ### 
 
    # Initialise ArgumentParser class
    ap = argparse.ArgumentParser()
    
    # Argument 1: Corpus
    ap.add_argument("-i", "--input_data", 
                    type = str,
                    required = False, # not required argument
                    help = "Define the input data",
                    default = "abcnews-date-text.csv")
    
    # Argument 2: Batch size
    ap.add_argument("-b", "--batch_size", 
                    type = int,
                    required = False, # not required argument
                    help = "Define the batch size, i.e. the number of headlines per batch",
                    default = 500)
    
    # Argument 3: Output filename
    ap.add_argument("-o", "--output_filename", 
                    type = str,
                    required = False, # not required argument
                    help = "Specify the name of the output file",
                    default = "headlines_sentiment_scores.csv")

    # Parse arguments
    args = vars(ap.parse_args())
    
    # Save input arguments
    input_data = os.path.join("..", "data", args["input_data"])
    batch_size = args["batch_size"]
    output_filename = args["output_filename"]
    
    # Create output directory if it does not already exist
    if not os.path.exists(os.path.join("..", "output")):
        os.mkdir(os.path.join("..", "output"))

    # Start message
    print("\n[INFO] Initializing sentiment analysis...")
    
    # Instantiate the Sentiment Analysis class
    sentiment_analysis = Sentiment_Analysis(input_data)
    
    # Prepare data
    print(f"\n[INFO] Preparing '{input_data}'...")
    data_df = sentiment_analysis.prepare_data()
    
    # Calculate sentiment scores
    print("\n[INFO] Calculating sentiment scores...")
    sentiment_scores = sentiment_analysis.calculate_sentiment_scores(data_df, batch_size)
    
    # Save sentiment scores as CSV-file to output directory
    print(f"\n[INFO] Saving sentiment scores as {output_filename} to 'output' directory...")
    sentiment_analysis.save_sentiment_scores(sentiment_scores, output_filename, data_df)
    
    # Creating rolling data, calculate rolling mean averages, and produce plots
    print("\n[INFO] Calculating rolling mean averages and generating plots...")
    rolling_data = sentiment_analysis.create_rolling_data(data_df, sentiment_scores)
     
    # Generate plot with 1-week rolling average
    sentiment_analysis.plot_rolling_averages(rolling_data, n_days = '7d')
        
    # Generate plot with 1-month rolling average
    sentiment_analysis.plot_rolling_averages(rolling_data, n_days = '30d')
    
    # Create sentiment barplot
    sentiment_analysis.create_sentiment_barplot(data_df)
    
    # User message 
    print(f"\n[INFO] Done! A CSV-file containing sentiment scores for each headline has been saved as {output_filename} to the 'output directory' together with plots displaying 1-week and 1-month rolling sentiment averages as well as a barplot showing the number of headlines for each sentiment category.\n")


### SENTIMENT ANALYSIS ###
    
# Creating Sentiment Analysis class 
class Sentiment_Analysis:

    # Intialize class
    def __init__(self, input_data):
        
        # Receive input
        self.data = input_data
   

    def prepare_data(self):
        """
        This method prepares the input data.
        """
        # Load data into dataframe
        data_df = pd.read_csv(self.data)
        data_df = data_df[:100]
    
        return data_df
        
        
    def calculate_sentiment_scores(self, data_df, batch_size):
        """
        This method calcualtes the sentiment scores. 
        """
        # Create empty list that we can append to in the loop
        sentiment_scores = []
    
        # Loop through each headline and calculate the sentiment score
        for headline in nlp.pipe(data_df["headline_text"], batch_size = batch_size):
            
            # Caclulate sentiment score for the headline
            sentiment = headline._.sentiment.polarity
            
            # Append to list
            sentiment_scores.append(sentiment)
            
        return sentiment_scores
           
        
    def save_sentiment_scores(self, sentiment_scores, output_filename, data_df):
        """
        This method saves the sentiment scores in a dataframe as a CSV-file to the output directory.
        """
        # Create a new column in the dataframe containing the sentiment scores using the insert() function
        data_df.insert(len(data_df.columns), "sentiment", sentiment_scores)
            
        # Specify output path
        output_path = os.path.join("..", "output", output_filename)
        
        # Save dataframe
        data_df.to_csv(output_path, index = False)
        
        
    def create_rolling_data(self, data_df, sentiment_scores):
        """
        This method calculates the rolling averages.
        """
         # In order to calculate the rolling averages, we need the dates as the index of the dataframe. Therefore, a new dataframe is created, and the dates are converted to datetime format and made the index of the dataframe
        rolling_data = pd.DataFrame({"sentiment": sentiment_scores}, 
                                    index = pd.to_datetime(data_df["publish_date"], 
                                                           format='%Y%m%d', 
                                                           errors='ignore'))
        
        return rolling_data
       
        
    def plot_rolling_averages(self, rolling_data, n_days):
        """
        This method creates plots displaying the rolling sentiment averages. 
        """
        # Calcuate sentiment scores with rolling averages of the number of days specified
        smoothed_sentiment = rolling_data.sort_index().rolling(n_days).mean()
        
        # Create plot
        plt.figure() 
        
        # Plot generated data
        plt.plot(smoothed_sentiment, label = f"Sentiment scores over time with a {n_days}-day rolling average")
        
        # Give plot a title
        plt.title(f"Sentiment over time with a {n_days} rolling average")
        
        # x-axis label
        plt.xlabel("Year") # x-label
        
        # Specify rotation of the x-axis labels so they do not overlap
        plt.xticks(rotation=45)
        
        # y-axis label
        plt.ylabel("Sentiment score")
        
        # Add legend
        plt.legend(loc = "upper right")
        
        # Save plot to output directory
        output_path = os.path.join("..", "output", f"smoothed_sentiment_{n_days}_rolling_average.png")
        plt.savefig(output_path, bbox_inches='tight')
        
        
    def create_sentiment_barplot(self, data_df):
        """
        This method creates a barplot using seaborn that displays the number of headlines for each sentiment category.
        """
        # Create new column for sentiment category
        data_df["sentiment_category"] = data_df["sentiment"]
        
        # Assign label (either negative, neutral or positive) to sentiment scores
        data_df["sentiment_category"] = np.where(data_df["sentiment"] > 0, "Positive", 
                                                 (np.where(data_df["sentiment"] < 0, "Negative", "Neutral")))
        
        # Count the number of headlines for each sentiment category
        counts_df = data_df.groupby("sentiment_category").count()
        
        # Reset index
        counts_df = counts_df.reset_index()
        
        # Plot headline counts for each sentiment category in seaborn barplot
        plot = sns.barplot(x="sentiment_category", y="sentiment" , data=counts_df, palette = ["red", "grey", "green"])
        
        # Set axis labels
        plot.set(xlabel="Sentiment", ylabel="Number of headlines")
        
        # Set title
        plot.set_title("Overview of Headline Sentiment")
        
        # Remove legend
        plot.legend([],[], frameon=False)
        
        # Save to output directory
        out_path = os.path.join("..", "output", "sentiment_barplot.png")
        plot = plot.get_figure()
        plot.savefig(out_path, bbox_inches='tight')
        
        
# Define behaviour when called from command line
if __name__=="__main__":
    main()