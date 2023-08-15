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
        title_tag = soup.find('title')

        # Extract the title and number issue
        title_text = title_tag.get_text(strip=True)
        issue_number = title_text.split(' · ')[1].split(' ')[1]
        title_issue = title_text.split(' · ')[0]

        # find author 
        author_tag = soup.find('a', class_='author Link--primary text-bold css-overflow-wrap-anywhere')
        username = author_tag.get_text(strip=True)
        # print(username)

        # find date comment
        date_comment = soup.find('relative-time')
        datetime_value = date_comment['datetime']
        datetime_obj = datetime.strptime(datetime_value, "%Y-%m-%dT%H:%M:%SZ")
        date_only = datetime_obj.date()

        comment_td = soup.find('td', class_='d-block comment-body markdown-body js-comment-body')
        comment_text = comment_td.get_text(strip=True)

        data.at[index, 'no isu'] = issue_number
        data.at[index, 'judul isu'] = title_issue
        data.at[index, 'author'] = username
        data.at[index, 'date'] = date_only
        data.at[index, 'comment'] = comment_text
        print(date_only)
    
    data.to_excel(excel_file_path, index=False)