import scrapy
import logging

class RatingsSpider(scrapy.Spider):
    name = 'ratings'
    download_delay = 1 
    
    def start_requests(self):
        urls = ['https://www.webtoons.com/en/genre']
        cookies = {
            'locale':'en',
            'needGDPR':'false',
            'needCCPA':'false' ,
            'needCOPPA':'false' ,
        }
        
        for url in urls:
            yield scrapy.Request(url=url, cookies=cookies,callback=self.parse)

    def parse(self, response):
        uls=response.css('ul.card_lst')
        links=[]
        for ul in uls:
            lis=ul.css('li')
            for li in lis:
                link=li.css('a').attrib['href']
                links.append(link)
                # logging.log(logging.DEBUG,link)
        
        for link in links:
            yield scrapy.Request(url=link,callback=self.parse_webtoon)
        
    def parse_webtoon(self,response):
        ul=response.css('ul.grade_area li')
        # logging.log(logging.DEBUG,ul.get())
        
        yield{
            'url':response.url,
            'title':response.css('h1.subj::text').get(),
            'genre':response.css('h2.genre::text').get(),
            'views':ul[0].css('em::text').get(),
            'rating':ul[2].css('em::text').get(),
        }
        
        
        