import json
import requests
# import urllib3
# import certifi
from typing import List, Dict
from bs4 import BeautifulSoup as bs
from bs4 import Tag, NavigableString


class Telegraph:
    def __init__(self, token, proxy):
        self.tags = {
            'a', 'aside', 'b', 'blockquote', 'br', 'code',
            'em', 'figcaption', 'figure', 'h3', 'h4', 'hr',
            'i', 'img', 'li', 'ol', 'p', 'pre',
            's', 'strong', 'u', 'ul', 'video'
        }
        self.publish_url = 'https://api.telegra.ph/createPage'
        self.token = token
        # self.spider = urllib3.PoolManager(cert_reqs="CERT_REQUIRED", ca_certs=certifi.where())
        self.spider = requests.Session()
        proxies = {
            'http': proxy,
            'https': proxy
        }
        self.publisher = requests.Session()
        if proxy:
            self.publisher.proxies = proxies

    def publish(self, title: str, author: str, content: List[Dict[str, str]]):
        '''
        :param title: str, title of telegraph page
        :param author: str, author of the page
        :param content: List[Node], a list of telegraph nodes.
            A telegraph node is a Dict including attributes of:
                tag (String)
                Name of the DOM element. Available tags:
                    a, aside, b, blockquote, br, code, em, figcaption,
                    figure, h3, h4, hr, i, iframe, img, li, ol, p, pre,
                    s, strong, u, ul, video.
                attrs (Object)
                    Optional. Attributes of the DOM element.
                    Key of object represents name of attribute,
                    value represents value of attribute.
                    Available attributes: href, src.
                children (Array of Node)
                    Optional. List of child nodes for the DOM element.
        '''
        content_str = json.dumps(content)
        fields = {
            'path': title,
            'return_content': 'true',
            'access_token': self.token,
            'title': title,
            'author_name': author,
            'content': content_str
        }
        # response = self.http.request('POST', self.publish_url, fields=fields).data.decode('utf-8')
        # response = json.loads(response)
        response = self.publisher.post(self.publish_url, data=fields).json()
        return response['result']['url']

    def tag2node(self, tag: Tag):
        node = dict()
        if type(tag) == NavigableString:
            return str(tag)
        tag_name = tag.name
        if tag_name == 'br' or tag_name == 'script':
            return ''
        if tag_name == 'iframe':
            node['tag'] = "a"
            node['attrs'] = tag.attrs
            node['attrs']['href'] = tag.attrs.get('data-src', tag.attrs.get('src', ''))
            node['children'] = [node['attrs']['href']]
            return node
        node['tag'] = tag_name if tag_name in self.tags else 'p'
        attrs = tag.attrs
        if 'display: none' in attrs.get('style', '') or \
            'visibility: hidden' in attrs.get('style', ''):
            attrs['hidden'] = 'True'
        try:
            del(attrs['style'])
        except KeyError:
            pass
        if tag_name == 'img':
            attrs['src'] = attrs.get('data-src', '')
        node['attrs'] = attrs

        if len(tag) > 0:
            node['children'] = [self.tag2node(t) for t in tag if t]
        return node

    def process_url(self, url: str):
        '''
        Return author, title and content from a given url
        '''
        # res = self.spider.request('get', url)
        # soup = bs(res.data.decode('utf-8'), features="html.parser")
        res = self.spider.get(url)
        soup = bs(res.text, features="html.parser")

        try:
            title = soup.select('#activity-name')[0].text.strip()
        except IndexError:
            title = 'Unknown Title'
            for t in ('title', 'h1', 'h2'):
                ele = soup.select(t)
                if ele and ele[0].text.strip():
                    title = ele[0].text.strip()
                    break
        try:
            author = soup.select('#js_name')[0].text.strip()
        except IndexError:
            author = 'Unknown Author'

        content = list()
        content_tags = soup.select('#js_content')
        for tag in content_tags:
            content.append(self.tag2node(tag))

        return {'title': title, 'author': author, 'content': content}


if __name__ == '__main__':
    ACCESS_TOKEN = ''
    tg = Telegraph(ACCESS_TOKEN, '')
    page = tg.process_url('')
    print(tg.publish(page['title'], page['author'], page['content']))
