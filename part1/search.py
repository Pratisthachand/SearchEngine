from wiki import article_titles, ask_search, ask_advanced_search

def search(keyword):
    res = []

    if keyword == '':
        return res
    else:
        for item in article_titles():
            if keyword.lower() in item.lower():
                res.append(item)
        return res

def title_length(max_length, titles):
    res = []

    for item in titles:
        if len(item) <= max_length:
            res.append(item) 
    return res

def article_count(count, titles):

    res = []

    if count > len(titles):
        return titles
    else:
        for step in range(count):
            res.append(titles[step])
        return res


def random_article(index, titles):
    if index < 0 or index > len(titles) - 1:
        return ''
    else:
        return titles[index]

def favorite_article(favorite, titles):

    for item in titles:
        if favorite.lower() == item.lower():
            return True
    return False

def multiple_keywords(keyword, titles):

    new_titles = search(keyword)
    titles.extend(new_titles)

    return titles

def display_result():
    # Stores list of articles returned from searching user's keyword
    articles = search(ask_search())

    # advanced stores user's chosen advanced option (1-5)
    # value stores user's response in being asked the advanced option
    advanced, value = ask_advanced_search()

    if advanced == 1:
        # value stores max article title length in number of characters
        # Update article titles to contain only ones of the maximum length
        articles = title_length(value, articles)
    if advanced == 2:
        # value stores max number of articles
        # Update article titles to contain only the max number of articles
        articles = article_count(value, articles)
    elif advanced == 3:
        # value stores random number
        # Update articles to only contain the article title at index of the random number
        articles = random_article(value, articles)
    elif advanced == 4:
        # value stores article title
        # Store whether article title is in the search results into a variable named has_favorite
        has_favorite = favorite_article(value, articles)
    elif advanced == 5:
        # value stores keyword to search
        # Updated article titles to contain article titles from the first search and the second search
        articles = multiple_keywords(value, articles)

    print()

    if not articles:
        print("No articles found")
    else:
        print("Here are your articles: " + str(articles))

    if advanced == 4:
        print("Your favorite article is" + ("" if has_favorite else " not") + " in the returned articles!")

if __name__ == "__main__":
    display_result()