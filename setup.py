import sys
from setuptools import setup, find_packages

if sys.version_info < (3, 6):
    raise Exception(
        "Python 3.6 or higher is required. Your version is %s." % sys.version
    )

__version__ = ""
exec(open('efb_mp_instantview_middleware/__version__.py').read())

long_description = open('README.md').read()

setup(
    name='efb-mp-instantview-middleware',
    packages=find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests"]
    ),
    version=__version__,
    description="WeChat Middleware of EH Forwarder Bot to enable instant\
        view for official accounts' articles",
    long_description=long_description,
    include_package_data=True,
    author='catbaron',
    author_email='catbaron@live.cn',
    url='https://github.com/catbaron0/efb-mp-instant-middleware',
    license='AGPLv3+',
    python_requires='>=3.6',
    keywords=[
        'ehforwarderbot', 'EH Forwarder Bot', 'EH Forwarder Bot Slave Channel',
        'wechat', 'weixin', 'chatbot'
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Communications :: Chat",
        "Topic :: Utilities"
    ],
    install_requires=[
        "ehforwarderbot>=2.0.0",
        "PyYaml",
        "bs4",
        "requests[socks]"
    ],
    entry_points={
        'ehforwarderbot.middleware': 'catbaron.mp_instantview = efb_mp_instantview_middleware:MPInstantViewMiddleware'
    }
)
