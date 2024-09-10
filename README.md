### Overview:

This Search Engine is a project designed to process and search through a dataset of article metadata. This project is divided into three parts, with Part 3 focusing on preprocessing metadata into dictionaries to enhance search efficiency. The search engine supports both basic and advanced search functionalities to find relevant articles based on user input.

### Functionality:

## Preprocessing

To improve search efficiency, we preprocess the metadata into dictionaries using the following functions:

- title_to_info(metadata): Converts the article metadata into a dictionary where each article title maps to its metadata (author, timestamp, and length).

- keyword_to_titles(metadata): Converts the article metadata into a dictionary where each keyword maps to a list of article titles that contain that keyword.

## Basic Search

The basic search functionality involves:

- User Input: Prompts the user for a keyword.
- Search Logic: Searches the preprocessed data for articles containing the user-provided keyword.
- Output: Returns a list of article titles where a match was found. If no results are found or if the user does not provide a keyword, returns an empty list.

## Advanced Search

After the basic search, users can perform advanced searches based on the following options:

- Article Title Length: Filters results to include only titles that do not exceed a specified maximum length.
- Key by Author: Returns a dictionary mapping authors to their articles.
- Filter to Author: Filters results to include only articles written by a specified author.
- Filter Out Keyword: Filters results to exclude articles containing a specified keyword.
- Articles from Year: Filters results to include only articles published in a specified year.
- None: No additional filtering; returns basic search results.

### Files:

`search.py`: performs a search (for any of the parts). To do so, input a word when prompted, choose an advanced option, and input an appropriate response to the advanced option question.

`wiki.py`: scraped article data from Wikipedia to be searched through

`search_tests.py`: unit and integration tests

`search_tests_helper.py`: helper functions for unit and integration tests
