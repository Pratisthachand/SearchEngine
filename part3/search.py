from wiki import article_metadata, ask_search, ask_advanced_search
import datetime
import time

def keyword_to_titles(metadata):
    dc = {}
    
    for article in metadata:
        if len(article) == 0:
            return {}

        title = article[0]
        keywords = article[4]

        for keyword in keywords:
            if keyword in dc:
                dc[keyword].append(title)
            else:
                dc[keyword] = [title]

    return dc
    
def title_to_info(metadata):
    outer_dc = {}

    for article in metadata:
        if len(article) == 0:
            return {}
            
        inner_dc = {}
        title = article[0]

        inner_dc['author'] = article[1]
        inner_dc['timestamp'] = article[2]
        inner_dc['length'] = article[3]

        outer_dc[title] = inner_dc

    return outer_dc

def search(keyword, keyword_to_titles):
    res = []

    for key in keyword_to_titles:
        if keyword == key:
            res.extend(keyword_to_titles[key])

    return res

'''
Functions 4-8 are called after searching for a list of articles containing the user's keyword.
'''

def article_length(max_length, article_titles, title_to_info):
    res = []
    for title in article_titles:
        if title_to_info[title]['length'] <= max_length:
            res.append(title)
    return res

def key_by_author(article_titles, title_to_info):
    dc = {}
    for title in article_titles:
        author = title_to_info[title]['author']
        if author in dc:
            dc[author].append(title)
        else:
            dc[author] = [title]
    return dc

def filter_to_author(author, article_titles, title_to_info):
    res = []
    for title in article_titles:
        if title_to_info[title]['author'] == author:
            res.append(title)
    return res

def filter_out(keyword, article_titles, keyword_to_titles):
    res = []
    
    for title in article_titles:
        contains_keyword = False
        for key in keyword_to_titles:
            if title in keyword_to_titles[key] and key == keyword:
                contains_keyword = True

        if contains_keyword == False:
            res.append(title)
    return res

def articles_from_year(year, article_titles, title_to_info):
    res = []
    if year <= 0:
        return []
        
    requested_date_start = datetime.date(year, 1, 1)
    requested_date_end = datetime.date(year, 12, 31)

    unix_timestamp_start = time.mktime(requested_date_start.timetuple())
    unix_timestamp_end = time.mktime(requested_date_end.timetuple())
    
    for title in article_titles:
        published_date = (title_to_info[title]['timestamp'])
        if published_date >= unix_timestamp_start and published_date <= unix_timestamp_end:
            res.append(title)
    return res

def display_result():
    # Preprocess all metadata to dictionaries
    keyword_to_titles_dict = keyword_to_titles(article_metadata())
    title_to_info_dict = title_to_info(article_metadata())
    
    # Stores list of articles returned from searching user's keyword
    articles = search(ask_search(), keyword_to_titles_dict)

    # advanced stores user's chosen advanced option (1-7)
    # value stores user's response in being asked the advanced option
    advanced, value = ask_advanced_search()

    if advanced == 1:
        # value stores max length of articles
        # Update articles to contain only ones not exceeding the maximum length
        articles = article_length(value, articles, title_to_info_dict)
    if advanced == 2:
        # Update articles to be a dictionary keyed by author
        articles = key_by_author(articles, title_to_info_dict)
    elif advanced == 3:
        # value stores author name
        # Update article metadata to only contain titles and timestamps
        articles = filter_to_author(value, articles, title_to_info_dict)
    elif advanced == 4:
        # value stores a second keyword
        # Filter articles to exclude those containing the new keyword.
        articles = filter_out(value, articles, keyword_to_titles_dict)
    elif advanced == 5:
        # value stores year as an int
        # Update article metadata to contain only articles from that year
        articles = articles_from_year(value, articles, title_to_info_dict)

    print()

    if not articles:
        print("No articles found")
    else:
        print("Here are your articles: " + str(articles))

if __name__ == "__main__":
    display_result()