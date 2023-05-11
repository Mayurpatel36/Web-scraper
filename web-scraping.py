#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 20:41:18 2023

@author: mayurpatel
"""

from bs4 import BeautifulSoup
import pandas as pd
import csv
import os
import re
from datetime import datetime
# Import the requests to gain access to a website and import beautiful soup which is a library designed for web scraping
import requests


#Set the working directory to a location of your preference
os.chdir('/Users/mayurpatel/Desktop/MMAI 5400/Assignment 1')

url = 'https://ca.trustpilot.com/review/squareup.com/ca'
resp = requests.get(url)

soup = BeautifulSoup(resp.text, 'html.parser')

# This is the html source
html_code = resp.text


# save it so that it can be viewed in an editor
with open('resp.html', 'w') as f:
    f.write(resp.text)

soup = BeautifulSoup(html_code, features='html.parser')

# Get the total number of reviews for the company
get_total_reviews = soup.find_all(
    class_='typography_body-l__KUYFJ typography_appearance-default__AAY17')
total_reviews = int(get_total_reviews[0].text.split()[0])


# This code gets the last page of reviews of the company we are scraping for
get_page_numbers = soup.find_all(
    class_='typography_heading-xxs__QKBS8 typography_appearance-inherit__D7XqR typography_disableResponsiveSizing__OuNP7')
last_page = int(get_page_numbers[-2].text)

# Create empty lists that will be used to store the data we extract
review_list = []
date_list = []
rating_list = []


# Get the reviews given by customers
block = soup.find_all(
    class_='paper_paper__1PY90 paper_outline__lwsUX card_card__lQWDv styles_reviewCard__hcAvl')


# This while loop starts at page one and will continue until the very last page of reviews for any given company
page = 1
while page != (last_page+1):
    url = f"https://ca.trustpilot.com/review/squareup.com/ca?page={page}"

    # Get the reviews given by customers
    block = soup.find_all(
        class_='paper_paper__1PY90 paper_outline__lwsUX card_card__lQWDv styles_reviewCard__hcAvl')

    for rating in range(0, len(block)):
        rating_block = block[rating].find_all(
            class_='star-rating_starRating__4rrcf star-rating_medium__iN6Ty')
        rate = rating_block[0].find('img')
        user_rating = int(re.findall(r'\d+', rate.get("alt"))[0])
        rating_list.append(user_rating)

    for review in range(0, len(block)):
        try:
            # Get the review block to see if there is a review
            review_block = block[review].find_all(
                class_='styles_reviewContent__0Q2Tg')
            # Exract the review from the tab
            review = review_block[0].find_all(
                class_='typography_body-l__KUYFJ typography_appearance-default__AAY17 typography_color-black__5LYEn')[0].text
            review_list.append(review)
        except IndexError:
            # Some customers leave only a title for their review but nothing in the body of the review
            # If there is no review the program will return an index error so for this error we will output N/A indicating no review in the body of the text
            review_list.append("N/A")

    for date in range(0, len(block)):
        dates = block[date].find_all(
            class_='typography_body-m__xgxZ_ typography_appearance-default__AAY17 typography_color-black__5LYEn')
        date_reviewed = dates[0].text.split(': ')[-1]
        # The date comes as a string. We need to convert it to a date type using datetime
        datetime_conv = datetime.strptime(date_reviewed, '%B %d, %Y')
        # Format the datetime converison to give the date in the desired output as stated in the assignment
        formatted_date = datetime_conv.strftime('%Y-%m-%dT%H:%M:%S%z')
        # Add the date to the list of dates when the review was made
        date_list.append(formatted_date)

    # Increment the page number on the while loop
    page += 1


# 1 Get company name
Company = soup.find_all(
    class_='typography_display-s__qOjh6 typography_appearance-default__AAY17 title_displayName__TtDDM')
# Extract the name of the company
# We will later need to use this company name to fill in the dataframe for all reviews
company_name = Company[0].text.strip()

# Assign an empty list that is the same length of the datapoints to the company name
name = []
for i in range(len(date_list)):
    name.append(company_name)


# Create the final dataframe as outlined in the assignment. We will then export this dataframe to a csv file.
output = pd.DataFrame(
    {'companyName': name,
     'datePublished': date_list,
     'ratingValue': rating_list,
     'reviewBody': review_list
     })


#output the dataframe into a csv with the location being the directory set at the start
output.to_csv('MMAI5400-A1.csv', index=False, encoding='utf-8')  
