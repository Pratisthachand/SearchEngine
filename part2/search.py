from wiki import article_metadata, ask_search, ask_advanced_search

def search(keyword):
    res = []
    for article in article_metadata():
        if keyword.lower() in article[4]:
            res.append(article[0:4])
    return res  

def article_length(max_length, metadata):
    res = []
    for article in metadata:
        if article[3] <= max_length:
            res.append(article[0:4])
    return res  

def unique_authors(count, metadata):
    author_list = []
    res = []

    if count <= 0:
        return res

    for article in metadata:
        if article[1].lower() not in author_list:
            author_list.append(article[1].lower())
            res.append(article)

    return res[:count]

def most_recent_article(metadata):
    latest = []
    max_time = 0

    for article in metadata:
        if max_time <= article[2]:
            max_time = article[2]
            latest = article

    return latest
    
def favorite_author(favorite, metadata):

    if len(favorite) == 0:
        return None

    for article in metadata:
        if favorite.lower() == article[1].lower():
            return True
    return False

def title_and_author(metadata):
    res = []
    for article in metadata:
        tuple = (article[0], article[1])
        res.append(tuple)
    return res

def refine_search(keyword, metadata):
    res = []
    res_from_basic_keyword = search(keyword)
    
    for article in metadata:
        if article in res_from_basic_keyword:
            res.append(article)
    return res

def display_result():
    # Stores list of articles returned from searching user's keyword
    articles = search(ask_search())

    # advanced stores user's chosen advanced option (1-7)
    # value stores user's response in being asked the advanced option
    advanced, value = ask_advanced_search()

    if advanced == 1:
        # value stores max article title length in number of characters
        # Update article metadata to contain only ones of the maximum length
        articles = article_length(value, articles)
    if advanced == 2:
        # value stores max number of unique authors
        # Update article metadata to contain only the max number of authors
        articles = unique_authors(value, articles)
    elif advanced == 3:
        # Update articles to only contain the most recent article
        articles = most_recent_article(articles)
    elif advanced == 4:
        # value stores author
        # Store whether author is in search results into variable named 
        # has_favorite
        has_favorite = favorite_author(value, articles)
    elif advanced == 5:
        # Update article metadata to only contain titles and authors
        articles = title_and_author(articles)
    elif advanced == 6:
        # value stores keyword to search
        # Update article metadata to contain only article metadata
        # that is contained in both searches
        articles = refine_search(value, articles)

    print()

    if not articles:
        print("No articles found")
    else:
        print("Here are your articles: " + str(articles))

    if advanced == 4:
        print("Your favorite author is" + ("" if has_favorite else " not") + " in the returned articles!")

if __name__ == "__main__":
    display_result()