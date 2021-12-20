# -*- coding: utf-8 -*-
# !/usr/bin/python3

# python3 -m pip install selenium --no-cache-dir

import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


def getQuotes(browser, url):
    browser.get(url)
    quotesLst = []
    gridItem = browser.find_elements_by_class_name("grid-item")

    for elem in gridItem:
        try:
            quoteText = elem.find_element_by_tag_name("div").text
            quotesLst.append(quoteText)
        except:
            continue

    return quotesLst


def setGForm(browser, quotes, author):

    GFormURL = ""

    for quote in quotes:
        browser.get(GFormURL)
        quoteTextBox = "quantumWizTextinputPaperinputInput"
        quoteTextBox = browser.find_elements_by_class_name(quoteTextBox)
        quoteTextBox[0].send_keys(quote)

        authorTextBox = "quantumWizTextinputPaperinputInput"
        authorTextBox = browser.find_elements_by_class_name(authorTextBox)
        authorTextBox[1].send_keys(author)

        submitBtn = "appsMaterialWizButtonPaperbuttonLabel"
        submitBtn = browser.find_element_by_class_name(submitBtn)
        submitBtn.click()


def main():
    options = Options()
    options.headless = True
    browser = webdriver.Firefox(options=options)

    authors = ["https://www.brainyquote.com/authors/charles-leclerc-quotes",
               "https://www.brainyquote.com/authors/mario-andretti-quotes",
               "https://www.brainyquote.com/authors/max-verstappen-quotes",
               "https://www.brainyquote.com/authors/lewis-hamilton-quotes",
               "https://www.brainyquote.com/authors/daniel-ricciardo-quotes",
               "https://www.brainyquote.com/authors/lando-norris-quotes",
               "https://www.brainyquote.com/authors/sebastian-vettel-quotes",
               "https://www.brainyquote.com/authors/murray-walker-quotes",
               "https://www.brainyquote.com/authors/gilles-villeneuve-quotes",
               "https://www.brainyquote.com/authors/valtteri-bottas-quotes",
               "https://www.brainyquote.com/authors/michael-schumacher-quotes",
               "https://www.brainyquote.com/authors/fernando-alonso-quotes",
               "https://www.brainyquote.com/authors/max-verstappen-quotes",
               "https://www.brainyquote.com/authors/ayrton-senna-quotes",
               "https://www.brainyquote.com/authors/jenson-button-quotes",
               "https://www.brainyquote.com/authors/sergio-perez-quotes",
               "https://www.brainyquote.com/authors/toto-wolff-quotes",
               "https://www.brainyquote.com/authors/mark-webber-quotes",
               "https://www.brainyquote.com/authors/sebastian-vettel-quotes",
               "https://www.brainyquote.com/authors/nelson-piquet-quotes",
               "https://www.brainyquote.com/authors/mick-schumacher-quotes",
               "https://www.brainyquote.com/authors/nico-hulkenberg-quotes",
               "https://www.brainyquote.com/authors/jackie-stewart-quotes",
               "https://www.brainyquote.com/authors/james-hunt-quotes",
               "https://www.brainyquote.com/authors/alain-prost-quotes",
               "https://www.brainyquote.com/authors/carlos-sainz-jr-quotes",
               "https://www.brainyquote.com/authors/lance-stroll-quotes",
               "https://www.brainyquote.com/authors/niki-lauda-quotes",
               "https://www.brainyquote.com/authors/nigel-mansell-quotes",
               "https://www.brainyquote.com/authors/nico-rosberg-quotes",
               "https://www.brainyquote.com/authors/juan-manuel-fangio-quotes",
               "https://www.brainyquote.com/authors/robert-kubica-quotes",
               "https://www.brainyquote.com/authors/damon-hill-quotes",
               "https://www.brainyquote.com/authors/stirling-moss-quotes",
               "https://www.brainyquote.com/authors/emerson-fittipaldi-quotes",
               "https://www.brainyquote.com/authors/felipe-massa-quotes",
               "https://www.brainyquote.com/authors/rubens-barrichello-quotes",
               "https://www.brainyquote.com/authors/john-surtees-quotes",
               "https://www.brainyquote.com/authors/bernie-ecclestone-quotes",
               "https://www.brainyquote.com/authors/romain-grosjean-quotes",
               "https://www.brainyquote.com/authors/christian-horner-quotes",
               "https://www.brainyquote.com/authors/mattia-binotto-quotes",
               "https://www.brainyquote.com/authors/guenther-steiner-quotes"]

    for authorURL in authors:
        quotes = getQuotes(browser, authorURL)
        author = authorURL.split("/")[-1].replace("-quotes", "").split("-")
        author = [name.capitalize() for name in author]
        author = " ".join(author)
        print(author)
        setGForm(browser, quotes, author)

    browser.close()


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
