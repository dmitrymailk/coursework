from bs4 import BeautifulSoup
import re
import pandas as pd
import json
import os
import requests
import pprint


class ScrapWebsite:
	def __init__(self):
		self.domain_name = "https://continuingstudies.uvic.ca"
		self.name = 'continuingstudies'
		self.column_names_list = ['link', 'level', 'name']
		self.column_names_texts = ['source_text', 'level', 'link', 'name', 'metadata']
		self.pages_list_urls = {
			'A1': "https://continuingstudies.uvic.ca/elc/studyzone/200/reading/",
			'A2': 'https://continuingstudies.uvic.ca/elc/studyzone/330/reading/',
			'B1': "https://continuingstudies.uvic.ca/elc/studyzone/410/reading/",
			'B2': "https://continuingstudies.uvic.ca/elc/studyzone/490/reading/",
		}
	
	def parse_pages_urls(self, page_list_url, level):
		page = requests.get(page_list_url)
		soup = BeautifulSoup(page.content, 'html5lib')
		tree_menu = soup.find('ul', attrs={'class': 'treemenu'})
		all_links = tree_menu.findAll('li', attrs={'class': 'treenode'})
		
		rows = []
		for item in all_links:
			if level != 'B2':
				article_link = item.find('ul').findAll('li')[0].find_all('a', href=True)[0]['href']
			else:
				article_link = item.find('ul').findAll('li')[1].find_all('a', href=True)[0]['href']
			
			article_link = self.domain_name + article_link
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
		dataframe_links = pd.read_csv("continuingstudies_links.csv")
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
		page = requests.get(url)
		soup = BeautifulSoup(page.content, 'html.parser')
		text = soup.find('div', attrs={'class': 'ReadingText'})
		text, audio_link = self.remove_trash(text)
		row = {
			'level': level,
			'source_text': text,
			'link': url,
			'name': self.name,
			'metadata': "{'audio_link': %s}" % audio_link
		}
		return row
	
	def remove_trash(self, text=None):
		new_text = str(text)
		regex_array = [
			r"<sup><strong>.<\/strong><\/sup>",
			r"(<([^>]+)>)",
			r"Your browser does not support the audio element, so here's a link to the mp3:",
			r"[’”“]",
			r"\n",
			r"(Credits:.*)"
		]
		for regex_str in regex_array:
			search_line = re.compile(regex_str)
			new_text = search_line.sub("", new_text).strip()
		
		audio_link = ""
		search_line = re.compile(r"(https.*\.mp3)")
		new_audio_link = search_line.findall(new_text)
		if len(new_audio_link) > 0:
			audio_link = new_audio_link[0]
		new_text = search_line.sub("", new_text).strip()
		
		return new_text, audio_link


if __name__ == '__main__':
	site_scrapper = ScrapWebsite()
	site_scrapper.get_all_texts()
# site_scrapper.get_all_links()
