from wiki import article_metadata, ask_search, ask_advanced_search
import datetime
import time


# Returns a dictionary mapping keyword to list of article titles in which the
# articles contain that keyword.

def keyword_to_titles(metadata):
    new_dictionary = {}
    for article in metadata:
        keywords = article.pop()
        title = article[0]
        for keyword in keywords:
            if keyword not in new_dictionary:
                new_dictionary[keyword] = [title]
            else:
                new_dictionary[keyword].append(title)

    return new_dictionary




# Returns a dictionary mapping article title to a dictionary with the following
# keys: author, timestamp, length of article.

def title_to_info(metadata):
    title_to_info_dict = {}
    for article in metadata:
        title = article[0]
        new_dictionary = {}
        new_dictionary['author'] = article[1]
        new_dictionary['timestamp'] = article[2]
        new_dictionary['length'] = article[3]
        title_to_info_dict[title] = new_dictionary

    return title_to_info_dict
    

# Returns a list of titles with articles containing the keyword, case-sensitive
# or an empty list if none are found.

def search(keyword, keyword_to_titles):
    titles = []
    for item in keyword_to_titles:
        title_list = keyword_to_titles[item]
        if keyword == item:
            titles.extend(title_list)
    return titles



# Returns a list of article titles from given titles for articles that do not
# exceed max_length number of characters.

def article_length(max_length, article_titles, title_to_info):
    new_list = []
    for title in article_titles:
        length = title_to_info[title]['length']
        if length > 0 and length <= max_length:
            new_list.append(title)

    return new_list


# Returns a dictionary that maps author to a list of all articles titles written
# by that author.

def key_by_author(article_titles, title_to_info):
    author_key = {}
    for title in article_titles:
        author = title_to_info[title]['author']
        if author in author_key:
            author_key[author].append(title)
        else:
            author_key[author] = [title]

    return author_key



# Returns a list of article titles from the initial search written by the author
# or an empty list if none.

def filter_to_author(author, article_titles, title_to_info):
    authors = key_by_author(article_titles, title_to_info)
    if author in authors:
        return authors[author]
    else:
        return []
    


# Returns a list of articles from the basic search that do not include a
# new keyword.
    
def filter_out(keyword, article_titles, keyword_to_titles):
    new_list = []
    
    if keyword in keyword_to_titles:
        titles_to_exclude = keyword_to_titles[keyword]
        for titles in article_titles:
            if titles not in titles_to_exclude:
                new_list.append(titles)
    else:
        new_list = article_titles

    return new_list



# Returns a list of article titles from the basic search that were published
# during the provided year.

def articles_from_year(year, article_titles, title_to_info):
    seconds = 31536000
    year_start = (year - 1970) * seconds
    year_end = year_start + seconds
    new_list = []

    for article in article_titles:
        timestamp = title_to_info[article]['timestamp']
        if timestamp >= year_start and timestamp <= year_end:
            new_list.append(article)

    return new_list


# Prints out articles based on searched keyword and advanced options
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