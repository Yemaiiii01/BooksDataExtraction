# Main Python script for scraping 
import requests
from bs4 import BeautifulSoup
import csv

# Function to scrape book details
def scrape_book_details(url):
    # Send a GET request to the product page
    response = requests.get(url)

    # Parse the HTML content of the page with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extracting the required details
    product_details = {
        'product_page_url': url,
        'universal_product_code': soup.find('th', text='UPC').find_next_sibling('td').text,
        'title': soup.find('div', class_='product_main').h1.text,
        'price_including_tax': soup.find('th', text='Price (incl. tax)').find_next_sibling('td').text,
        'price_excluding_tax': soup.find('th', text='Price (excl. tax)').find_next_sibling('td').text,
        'quantity_available': soup.find('th', text='Availability').find_next_sibling('td').text.split('(')[1].split(' ')[0],  # Extracting number from the string
        'product_description': soup.find('meta', attrs={'name': 'description'})['content'].strip(),
        'category': soup.find('ul', class_='breadcrumb').find_all('li')[2].text.strip(),
        'review_rating': soup.find('p', class_='star-rating')['class'][1],
        'image_url': soup.find('img')['src'].replace('../../', 'http://books.toscrape.com/')
    }
    
    return product_details

# Define the CSV file name
csv_file = 'book_details.csv'

# Function to save details to CSV
def save_to_csv(data, file_name):
  # Field names for CSV
    fields = ['product_page_url', 'universal_product_code', 'title', 'price_including_tax',
              'price_excluding_tax', 'quantity_available', 'product_description', 'category', 
              'review_rating', 'image_url']
    
    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerow(data)

# URL of the book to scrape
book_url = "https://books.toscrape.com/catalogue/the-most-perfect-thing-inside-and-outside-a-birds-egg_938/index.html"

# Scrape the book details
book_details = scrape_book_details(book_url)

# Save the book details to CSV
save_to_csv(book_details, csv_file)

print(f"Book details saved to {csv_file}")
import requests
from bs4 import BeautifulSoup
import csv

# Function to fetch book URLs from a single category
def fetch_book_urls(category_url):
    book_urls = []
    while True:
        response = requests.get(category_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        books = soup.find_all('h3')
        for book in books:
            book_url = book.find('a')['href'].replace('../../../', 'http://books.toscrape.com/catalogue/')
            book_urls.append(book_url)

        # Check if there is a next page
        next_button = soup.find('li', class_='next')
        if next_button:
            next_page_url = next_button.find('a')['href']
            category_url = '/'.join(category_url.split('/')[:-1]) + '/' + next_page_url
        else:
            break
    return book_urls

# Function to scrape book details from Phase 1
def scrape_book_details(url):
    # The rest of the scraping code from Phase 1 goes here
    # ...
    pass  # Replace with the actual scraping code

# The chosen category URL (example: science category)
category_url = 'http://books.toscrape.com/catalogue/category/books/science_22/index.html'

# Fetch all book URLs in the chosen category
book_urls = fetch_book_urls(category_url)

# List to store all books' details
books_data = []

# Iterate over each book URL and scrape details
for book_url in book_urls:
    book_details = scrape_book_details(book_url)
    books_data.append(book_details)

# CSV file path to save the details
csv_file_path = 'category_books_details.csv'

# Save all book details into a single CSV file
fields = ['product_page_url', 'universal_product_code', 'title', 'price_including_tax',
          'price_excluding_tax', 'quantity_available', 'product_description', 'category', 
          'review_rating', 'image_url']

with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fields)
    writer.writeheader()
    for book_data in books_data:
        writer.writerow(book_data)

print(f"All book details from the category have been saved to {csv_file_path}")
