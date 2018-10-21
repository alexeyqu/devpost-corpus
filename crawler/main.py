import sys

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from tagger.tagger import Tagger


if __name__ == '__main__':
    stage = 'help'
    if len(sys.argv) > 1:
        stage = sys.argv[1]
    if stage == 'help':
        print('\n'.join([
            'Devpost Corpora Builder usage:',
            '  $ python '+ str(sys.argv[0]) + ' <stage> [args]',
            'available stages:',
            '  help: print this msg and exit',
            '  crawler: start Scrapy devpost crawler',
            '  tagger: perform tokenization and tagging on crawled data']))
            
    elif stage == 'crawler':
        process = CrawlerProcess(get_project_settings())
        process.crawl('projects')
        process.start()
    elif stage == 'tagger':
        tagger = Tagger(get_project_settings())
        tagger.make_tagging()
                
