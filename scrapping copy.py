from bs4 import BeautifulSoup
import requests
import pandas as pd
from openpyxl import load_workbook
from datetime import datetime


excel_file_path = 'list-github.xlsx'

data = pd.read_excel(excel_file_path)
for index, row in data.iterrows():
    link_github = row['link'] 
    # print({link_github})

    response = requests.get(link_github)
    if response.status_code == 200:
        # perhatikan sensitive case ( saat link disertai dengan spasi, maka akan error. 
        # contoh : 'https://github.com/pkp/pkp-lib/issues/5185 ')
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the <title> tag
     # Find the issue number outside of the 'edit-comment-hide' class
        issue_number_element = soup.find('span', class_='f1-light color-fg-muted')
        if issue_number_element:
                issue_number = issue_number_element.get_text(strip=True)
        else:
            issue_number = None

            # Find the username element
        username_element = soup.find('a', class_='author Link--primary text-bold css-overflow-wrap-anywhere')
        if username_element:
            username = username_element.get_text(strip=True)
        else:
            username = None

            # Find the related link
        related_link_element = soup.find('a', class_='class-for-related-link')
        if related_link_element:
            related_link = related_link_element['href']  # Extract the href attribute
        else:
            related_link = None

        comment_divs = soup.find_all('div', class_='edit-comment-hide')

            # Keep track of comment count for each issue number
        comment_count = 0

        for comment_div in comment_divs:
            if comment_count >= 3:
                break  # Limit comments to 3 per issue number

            comment_paragraphs = comment_div.find_all(['p', 'ol'])
            comments_text = []

            for paragraph in comment_paragraphs:
                    if paragraph.name == 'p':
                        comment_text = paragraph.get_text(strip=True)
                        # Remove URLs from the comment text
                        comment_text = re.sub(r'http\S+', '', comment_text)
                        comments_text.append(comment_text)
                    elif paragraph.name == 'ol':
                        list_items = paragraph.find_all('li')
                        list_text = "\n".join(item.get_text(strip=True) for item in list_items)
                        # Remove URLs from the list text
                        list_text = re.sub(r'http\S+', '', list_text)
                        comments_text.append(list_text)

            if comments_text:
                    comments = "\n\n\n".join(comments_text)
                    data.append({
                        'issue_number': issue_number,
                        'username': username,
                        'comments': comments,
                        'related_link': related_link,

                    })

                    comment_count += 1
    
    data.to_excel(excel_file_path, index=False)





# Baca isi file HTML
# file_path = "Geometry.html"
# with open(file_path, "r", encoding="utf-8") as file:
#     html_content = file.read()

# # Lakukan web scraping menggunakan BeautifulSoup
# soup = BeautifulSoup(html_content, "html.parser")
# author_link = soup.find("a", {"class": "author"})
# content_tag = soup.find('p', dir='auto')

# # Cek apakah data "fefespn" berhasil ditemukan
# if author_link:
#     data = {
#         "username": author_link.text.strip(),
#         "content": content_tag.text.strip(),
#         "profile_url": "https://github.com" + author_link["href"]
#     }
#     print(data)
# else:
#     print("Data fefespn tidak ditemukan.")
