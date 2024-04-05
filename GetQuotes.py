# -*- coding: utf-8 -*-
# !/usr/bin/python3

# python3 -m pip install selenium --no-cache-dir

import os

from selenium import webdriver
from selenium.webdriver.firefox.options import Options


def getQuotes(browser, url):
    """
    A function that takes a browser instance and a URL, navigates to the URL using the browser,
    finds all elements with class name "grid-item", extracts the text from their child div elements,
    and returns a list of the extracted texts.

    Parameters:
    browser (selenium.webdriver.chrome.webdriver.WebDriver): A Selenium WebDriver instance used to navigate to the URL.
    url (str): A URL to navigate to using the browser.

    Returns:
    list: A list of strings representing the text content of the div elements inside each "grid-item" element.
    """
    # Navigate to the URL using the browser
    browser.get(url)

    # Create an empty list to store the extracted quotes
    quotesLst = []

    # Find all elements with class name "grid-item"
    gridItem = browser.find_elements_by_class_name("grid-item")

    # Loop through each "grid-item" element
    for elem in gridItem:
        try:
            # Extract the text content of the child div element
            quoteText = elem.find_element_by_tag_name("div").text
            # Add the extracted text to the list of quotes
            quotesLst.append(quoteText)
        except:
            # If an exception occurs (e.g. if the "grid-item" element doesn't have a child div element), continue to the next element
            continue

    # Return the list of extracted quotes
    return quotesLst


def setGForm(browser, quotes, author):
    """
    This function sets the quote and author fields in a Google Form using Selenium WebDriver.

    Args:
        browser (webdriver object): an instance of Selenium WebDriver
        quotes (list of str): a list of quotes to enter in the form
        author (str): the name of the author to enter in the form

    Returns:
        None
    """

    # Initialize the Google Form URL
    GFormURL = ""

    # Loop through each quote in the list
    for quote in quotes:
        # Load the Google Form URL in the browser
        browser.get(GFormURL)

        # Find the quote text box and enter the quote
        quoteTextBox = "quantumWizTextinputPaperinputInput"
        quoteTextBox = browser.find_elements_by_class_name(quoteTextBox)
        quoteTextBox[0].send_keys(quote)

        # Find the author text box and enter the author's name
        authorTextBox = "quantumWizTextinputPaperinputInput"
        authorTextBox = browser.find_elements_by_class_name(authorTextBox)
        authorTextBox[1].send_keys(author)

        # Find the submit button and click it
        submitBtn = "appsMaterialWizButtonPaperbuttonLabel"
        submitBtn = browser.find_element_by_class_name(submitBtn)
        submitBtn.click()


def main():
    """Scrapes quotes from a list of authors' pages on brainyquote.com
    and adds them to a Google Form using Selenium WebDriver.

    Returns:
    None
    """

    # Set headless browsing and open Firefox browser
    options = Options()
    options.headless = True
    browser = webdriver.Firefox(options=options)

    # List of authors' pages to scrape quotes from
    authors = [...]

    # Loop through authors and add their quotes to the Google Form
    for authorURL in authors:
        quotes = getQuotes(browser, authorURL)
        author = authorURL.split("/")[-1].replace("-quotes", "").split("-")
        author = [name.capitalize() for name in author]
        author = " ".join(author)
        print(author)
        setGForm(browser, quotes, author)

    # Close the browser
    browser.close()


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
