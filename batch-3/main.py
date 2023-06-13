"""
调试启动main文件
"""

from scrapy.cmdline import execute
import os
import sys

if __name__ == '__main__':
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    # execute(['scrapy', 'crawl', 'a_stranger'])
    execute(['scrapy', 'crawl', 'huoxing'])
    # execute(['scrapy', 'crawl', 'download_user_images'])

