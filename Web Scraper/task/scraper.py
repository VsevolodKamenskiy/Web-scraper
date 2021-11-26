import requests, re, os
from bs4 import BeautifulSoup


# get file name
def get_file_name(name: str):
    regex_pattern = '[!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]'
    file_name = re.sub(regex_pattern, '', name)
    file_name = re.sub(' ', '_', file_name) + '.txt'
    return file_name


def page_parser(url: str, params: dict, cat: str, pages: int):

    saved_articles = 0

    for current_page in range(1, pages + 1):

        # links to articles
        links = list()

        # update our params for URL of current page
        params.update({'page': current_page})

        response = requests.get(url, params)

        # if not 200
        if not response:
            return 'The URL {0} returned {1}!'.format(response.url, response.status_code)

        # make the current page directory for files
        try:
            os.mkdir('Page_{0}'.format(current_page))
        except OSError:
            pass

        # initialize parser
        soup = BeautifulSoup(response.content, 'html.parser')

        # find all articles on the page
        articles = soup.find_all('article')

        for item in articles:

            # find a type of an article
            result = item.find('span', {'class': 'c-meta__type'}).get_text()

            # if it's our category, then save link to the article
            if result == cat:
                links.append('https://www.nature.com' + item.find('a').get('href'))

        for link in links:
            article_response = requests.get(link)

            if not article_response:
                return 'The URL {0} returned {1}!'.format(link, article_response.status_code)

            # initialize a parser for article
            article_soup = BeautifulSoup(article_response.content, 'html.parser')

            # generate file name
            file_name = get_file_name(article_soup.find('h1').get_text())

            # get absolute path to file
            path = os.path.join(os.getcwd(), 'Page_{0}'.format(current_page), file_name)

            # open a file for saving in binary mode
            fl = open(path, 'wb')

            # TO DO
            # add more categories
            #
            # parsing depends on category, because article contents are in different tags
            if cat in {'News', 'Career Column', 'Nature Briefing', 'Correspondence', 'Nature Careers Podcast', 'Outlook'}:
                fl.write(article_soup.find('div', {'class': 'c-article-body'}).get_text().encode(encoding='utf-8'))
            elif cat == 'Article':
                fl.write(article_soup.find('div', {'class': 'c-article-section__content'}).get_text().encode(encoding='utf-8'))

            saved_articles += 1
            fl.close()

    return 'Saved all articles: {0}'.format(saved_articles)


if __name__ == '__main__':
    page_number = (int(input()))
    category = input()

    url = 'https://www.nature.com/nature/articles'
    params = {'sort': 'PubDate', 'year': '2020'}

    print(page_parser(url, params, category, page_number))

