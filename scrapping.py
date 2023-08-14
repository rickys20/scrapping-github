from bs4 import BeautifulSoup
import requests
import pandas as pd
from openpyxl import load_workbook

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
        title_tag = soup.find('title')
        # Extract the title
        title_text = title_tag.get_text(strip=True)
        issue_number = title_text.split(' · ')[1].split(' ')[1]
        title_issue = title_text.split(' · ')[0]

        author_tag = soup.find('a', class_='author Link--primary text-bold css-overflow-wrap-anywhere')

        # Extract the author's username and full name from the tag attributes
        username = author_tag.get_text(strip=True)
        print(username)

        data.at[index, 'no isu'] = issue_number
        data.at[index, 'judul isu'] = title_issue
        data.at[index, 'author'] = username
        # print(issue_number)
    
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
