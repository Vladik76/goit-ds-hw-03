import requests, json
from bs4 import BeautifulSoup

quotes = []
authors = []


def scrap_page(index: int):
    url = f'https://quotes.toscrape.com/page/{index}/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    for el in soup.find_all('div', class_='quote'):
        author = el.find('small', class_='author')
        tags = el.find_all('a', class_='tag')
        tagslist = [tag.text for tag in tags]
        quote = el.find('span', class_='text')
        quotes.append(
            {
                "tags": tagslist,
                "author": author.text,
                "quote": quote.text
            }
        )
        # Now we get details about author
        author_url = author.find_next_sibling('a').get('href')
        if author_url:
            url1 = f'https://quotes.toscrape.com{author_url}'
            response1 = requests.get(url1)
            soup1 = BeautifulSoup(response1.text, 'lxml')
            born_date = soup1.find('span', class_='author-born-date').text
            born_location = soup1.find('span', class_='author-born-location').text
            auth_description = soup1.find('div', class_='author-description').text.strip()

            author = {
                "fullname" : author.text,
                "born_date" : born_date,
                "born_location" : born_location,
                "description" : auth_description
            }

            # add to list if not already in authors list
            if author not in authors:
                authors.append(author)



    # if we find NEXT button we can scrap next page
    if soup.find('li', class_='next'):
        index += 1
        scrap_page(index)
    else:
        with open('quotes.json', 'w') as f:
            json.dump(quotes, f, indent=4)

        with open('authors.json', 'w') as f:
            json.dump(authors, f, indent=4)


if __name__ == "__main__":
    scrap_page(1)
