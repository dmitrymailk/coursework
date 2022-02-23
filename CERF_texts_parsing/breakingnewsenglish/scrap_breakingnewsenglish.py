from bs4 import BeautifulSoup
import re
import pandas as pd
import json
import os
import requests


class ScrapWebsite:
	def __init__(self):
		self.domain_name = "https://breakingnewsenglish.com/"
		self.name = 'breakingnewsenglish'
		self.column_names_list = ['link', 'level', 'name']
		self.column_names_texts = ['source_text', 'level', 'link', 'name', 'metadata']
		self.pages_list_urls = {
			'A1': "./A1.html",
			'A2': './A2.html',
			'B1': "./B1.html",
			'B2': "./B2.html",
		}
	
	def parse_pages_urls(self, page_list_url, level):
		page = open(page_list_url, encoding='utf-8').read()
		soup = BeautifulSoup(page, 'html.parser')
		links = soup.find('div', attrs={'id': 'primary'}) \
			.find('div', attrs={'class': 'content-container'}) \
			.find('ul', attrs={'class': 'list-class'}).find_all('a', href=True)
		
		rows = []
		for item in links:
			article_link = self.domain_name + item['href']
			row = { 
				'link': article_link,
				'level': level,
				'name': self.name
			}
			rows.append(row)
		return rows
	
	def get_all_links(self):
		dataframe = pd.DataFrame(columns=self.column_names_list)
		
		for level, list_url in self.pages_list_urls.items():
			texts_links = self.parse_pages_urls(list_url, level)
			for item in texts_links:
				dataframe = dataframe.append(item, ignore_index=True)
		
		dataframe.to_csv(f"{self.name}_links.csv", index=False)
		print('OK. Links parsed.')
	
	def get_all_texts(self):
		dataframe_links = pd.read_csv(f"{self.name}_links.csv")
		dataframe_texts = pd.DataFrame(columns=self.column_names_texts)
		data_len = len(dataframe_links)
		for i in range(data_len):
			# print(row)
			row = dataframe_links.iloc[i]
			level = row['level']
			link = row['link']
			new_row = self.scrap_one_page(link, level)
			dataframe_texts = dataframe_texts.append(new_row, ignore_index=True)
		dataframe_texts.to_csv(f'{self.name}_texts.csv', index=False)
		print('OK. Texts Parsed.')
	
	def scrap_one_page(self, url, level):
		headers = {
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
		page = requests.get(url, headers=headers)
		soup = BeautifulSoup(page.content, 'html.parser')
		text = soup.find('article')
		if text:
			text = text.get_text()
			text = self.remove_trash(text)
		else:
			text = ''
		row = {
			'level': level,
			'source_text': text,
			'link': url,
			'name': self.name,
			'metadata': ""
		}
		return row
	
	def remove_trash(self, text=None):
		new_text = str(text)
		new_text = text.replace("\n", '')
		return new_text


if __name__ == '__main__':
	site_scrapper = ScrapWebsite()
	# links = site_scrapper.parse_pages_urls('./A2.html', 'A1')
	# print(links)
	site_scrapper.get_all_texts()
# site_scrapper.get_all_links()
