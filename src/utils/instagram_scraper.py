from random import choice
import json
from bs4 import BeautifulSoup
import requests

# this file is not used in the current pipeline
# is only capable of retrieving the images displayed on the first page (without scrolling)
# the current pipeline uses the infinite_scraper file which is based on Instagram's private API

headers={'User-Agent':  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
         ,  'content-type': 'application/json'
         , 'accept-encoding': 'gzip, deflate, br'
         , 'cache-control': 'no-cache'
         , 'accept' : '*/*'
         , 'accept-language' : 'de-DE, de; q=0.9,en-US; q=0.8,en;q=0.7'
         #, 'referer' : url
         , 'connection' : 'keep-alive'
         , 'cookie' : 'ig_cb=1; ig_did=DA66C494-9DFE-48F6-BA63-66F11DF8EC03; csrftoken=ukE8jYSjQxVs1YGPYddEkAXsN6WZ4Qmw; mid=XoChrAALAAG78Upva7Ld0TAzeTtm; rur=ASH; urlgen="{\"2a04:ee41:4:95:91f9:b9d4:8aab:41c\": 15796\054 \"213.55.241.7\": 15796\054 \"2a04:ee41:4:95:60ae:def3:2fd7:3633\": 15796}:1jIpww:PTjjrSzpjC6dWww8-AVOnfdQAFA"'
        }
_user_agents = [
   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
]


class InstagramScraper:

    def __init__(self, user_agents=None, proxy=None):
        self.user_agents = user_agents
        self.proxy = proxy

    def __random_agent(self):
        if self.user_agents and isinstance(self.user_agents, list):
            return choice(self.user_agents)
        return choice(_user_agents)

    def __request_url(self, url):
        """Our second helper method is simply a wrapper around requests.
        We pass in a URL and try to make a request using the provided user agent and proxy.
        If we are unable to make the request or Instagram responds with a non-200 status code we simply re-raise the error.
        If everything goes fine, we return the page in questions HTML."""
        try:
            response = requests.get(url, headers={'User-Agent': self.__random_agent()},
                                    proxies={'http': self.proxy, 'https': self.proxy})
            # response = requests.get(url, headers=headers, proxies={'http': self.proxy, 'https': self.proxy})
            response.raise_for_status()
        except requests.HTTPError:
            raise requests.HTTPError('Received non 200 status code from Instagram')
        except requests.RequestException:
            raise requests.RequestException('Internet connection failed.')
        else:
            return response.text

    @staticmethod
    def extract_json_data(html):
        """Instagram serve’s all the of information regarding a user in the form of JavaScript object.
        This means that we can extract all of a users profile information and their recent posts by just
        making a HTML request to their profile page. We simply need to turn this JavaScript object into
        JSON, which is very easy to do."""
        soup = BeautifulSoup(html, 'html.parser')
        body = soup.find('body')
        script_tag = body.find('script')
        content = script_tag.contents
        content_string = ''.join(content)
        raw_string = content_string.strip().replace('window._sharedData =', '').replace(';', '')
        return json.loads(raw_string)

    def profile_page_metrics(self, profile_url):
        results = {}
        try:
            response = self.__request_url(profile_url)
            json_data = self.extract_json_data(response)
            metrics = json_data['entry_data']['ProfilePage'][0]['graphql']['user']
        except Exception as e:
            raise e
        else:
            for key, value in metrics.items():
                if key != 'edge_owner_to_timeline_media':
                    if value and isinstance(value, dict):
                        value = value['count']
                        results[key] = value
                    elif value:
                        results[key] = value
        return results

    def hash_page_metrics(self, profile_url):
        results = {}
        try:
            response = self.__request_url(profile_url)
            json_data = self.extract_json_data(response)
            metrics = json_data['entry_data']['TagPage'][0]['graphql']['hashtag']

        except Exception as e:
            raise e
        else:
            for key, value in metrics.items():
                if key != 'edge_hashtag_to_media' and key != 'edge_hashtag_to_top_posts' and key != 'profile_pic_url':
                    results[key] = value
                    if value and isinstance(value, dict):
                        try:
                            value = value['count']
                            results[key] = value
                        except:
                            results[key] = value
                        try:
                            sigma = []
                            for i in range(0, 5):
                                value = value['edges'][i]['node']['name']
                            sigma.append(value)
                            print(len(value['edges']['node']))

                        except:
                            results[key] = value
                    elif value:
                        results[key] = value
        return results

    def profile_page_posts(self, profile_url):
        results = []
        try:
            response = self.__request_url(profile_url)
            json_data = self.extract_json_data(response)
            metrics = json_data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media'][
                "edges"]
        except Exception as e:
            raise e
        else:
            for node in metrics:
                node = node.get('node')
                # if node and isinstance(node, dict): #this line only gets most recent post out
                results.append(node)
        return results

    def hashtag_page_posts(self, hashtag_url):
        results = []
        try:
            response = self.__request_url(hashtag_url)
            json_data = self.extract_json_data(response)
            metrics = json_data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']["edges"]
        except Exception as e:
            raise e
        else:
            for node in metrics:
                node = node.get('node')
                # if node and isinstance(node, dict): #this line only gets most recent post out
                results.append(node)
        return results