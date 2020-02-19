# coding: utf-8
import logging
import threading
from pathlib import Path
from typing import Any, Dict, Optional
from concurrent.futures import ThreadPoolExecutor
import urllib

import yaml

from ehforwarderbot import coordinator, Middleware, Message, MsgType
from ehforwarderbot.utils import get_config_path
from . import __version__ as version
from .telegraph import Telegraph


class MPInstanceViewMiddleware(Middleware):
    """
    Middleware - MP InstanceView Middleware
    Convert Wechat Official Accounts' url to telegraph to enable
    instance viewl.
    Author: Catbaron <https://github.com/catbaron0>, 
    """

    middleware_id: str = "catbaron.mp_instanceview"
    middleware_name: str = "MP InstanceView Middleware"
    __version__ = version.__version__
    logger: logging.Logger = logging.getLogger(
        "plugins.%s.MPInstanceViewMiddleware" % middleware_id)

    def __init__(self, instance_id: str = None):
        super().__init__()
        self.config: Dict[str: Any] = self.load_config()
        token: str = self.config.get("telegraph_token")
        self.telegraph = Telegraph(token)

    def load_config(self) -> Optional[Dict]:
        config_path: Path = get_config_path(self.middleware_id)
        if not config_path.exists():
            self.logger.info('The configure file does not exist!')
            return
        with config_path.open('r') as f:
            d: Dict[str, Any] = yaml.load(f)
            if not d:
                self.logger.info('Load configure file failed!')
                return
            return d

    @staticmethod
    def is_mp(message: Message) -> bool:
        if not message.attributes:
            return False
        if not message.chat.vendor_specific.get('is_mp', False):
            return False
        url = message.attributes.url
        if url and url.startswith('https://mp.weixin.qq.com/'):
            return True
        if url and url.startswith('http://mp.weixin.qq.com/'):
            return True
        return False

    def process_message(self, message: Message) -> Optional[Message]:
        """
        Process a message with middleware
        Args:
            message (:obj:`.Message`): Message object to process
        Returns:
            Optional[:obj:`.Message`]: Processed message or None if discarded.
        """
        if message.deliver_to != coordinator.master:
            return message
        if message.author.name == 'You':
            return message
        if not self.is_mp(message):
            return message
        # threading.Thread(
        #     target=self.process_url,
        #     args=(message,),
        #     name=f"MPInstanceView thread {message.uid}"
        #     ).start()
        message = self.process_url(message)
        return message

    def process_url(self, message: Message):
        try:
            mp_url = message.attributes.url
            page = self.telegraph.process_url(mp_url)
            url = self.telegraph.publish(
                page['title'],
                page['author'],
                page['content']
            )
            title = message.attributes.title
            desc = message.attributes.description
            message.attributions = None
            message.text = f"{title}\n{desc}\n{url}\n{mp_url}"
            message.type = MsgType.Text
        except Exception:
            self.logger.info('Failed to process mp url!')
            return
        return message
        # message.edit = True
        # message.edit_media = False
        # coordinator.send_message(message)
