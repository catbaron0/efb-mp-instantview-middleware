import json
import requests
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
        # self.http = urllib3.PoolManager(
        #     cert_reqs="CERT_REQUIRED",
        #     ca_certs=certifi.where()
        # )
        proxies = {
            'http': proxy,
            'https': proxy
        }
        self.publisher = requests.Session()
        self.spider = requests.Session()
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
        if tag_name == 'br':
            return ''
        node['tag'] = tag_name if tag_name in self.tags else 'p'
        attrs = tag.attrs
        if 'display: none' in attrs.get('style', '') or \
            'visibility: hidden' in attrs.get('style', ''):
            attrs['hidden'] = 'True'
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
    ACCESS_TOKEN = '1acbef8d50b3ba8d0d0db262a413f545320d335fae6dc4cc4a860f7c6c26'
    tg = Telegraph(ACCESS_TOKEN)
    page = tg.process_url(
        # 'https://mp.weixin.qq.com/s?__biz=MjM5NzE1NTMyNg==&mid=2650934190&idx=5&sn=72c8016694181b337a48fba178a26355&chksm=bd28f33f8a5f7a29bd27494dbf06859aad5ce0a663eef46fa2e5443a3774b7fbec82a91522ed&scene=0&xtrack=1#rd'
        # 'https://mp.weixin.qq.com/s?__biz=MzUwOTg3NjIwNg==&mid=2247525393&idx=5&sn=77089269b97ed4a96a835a3ca0747b30&chksm=f909a690ce7e2f86a320136b7f6b7b6dc29d6c89585c6b5610ab8709687e7b238078a51e557f&scene=0&xtrack=1#rd'
        'http://mp.weixin.qq.com/s?__biz=MjM5NzE1NTMyNg==&mid=2650934220&idx=1&sn=8f02f1efa9963fa787484e0ca86101f5&chksm=bd28f35d8a5f7a4be54547d04fc1df0069970685b3d33f69c4433c5f35e370f138fac62864fa&scene=0&xtrack=1#rd'
    )
    print(tg.publish(page['title'], page['author'], page['content']))
