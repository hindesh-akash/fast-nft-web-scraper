import scrapy
import pandas as pd
import time
#In this implementation I have used scrapy spider to scrape the websites.
# This approach is much faster than previous one.

class Nftscraperv1Spider(scrapy.Spider):
    name = "nftscraperv3"
    # start_urls = ["https://raritysniper.com/nft-collections"]

    link_data = pd.read_csv('all_nft_collections.csv')
    all_links = link_data['collection_name'].tolist()

    start_urls = all_links

    headers_nft = {'Referer': 'https://raritysniper.com/',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
    

    def parse(self, response):

        for slug in response.url:
            self.url = f"https://api.raritysniper.com/public/collection/{slug}"
            time.sleep(0.5)
            yield scrapy.Request(
                url=self.url,
                callback=self.parse_json,
                headers=self.headers_nft
            )

    def parse_json(self, response):
        data = response.json() 

        no_of_nfts = data["totalSupply"]
        collect_name = self.url.split('/')[-1]
        for i in range(no_of_nfts):
            time.sleep(0.5)
            yield scrapy.Request(
                f"https://api.raritysniper.com/public/collection/{collect_name}/id/{i}",
                callback=self.parse_nft,
                headers=self.headers_nft
            )

    def parse_nft(self, response):
        data = response.json() 
        yield {
            "NFT_ID": data["nftId"],
            "RANK": data["rank"],
            "rarityScore": data["rarityScore"],
            "collectionName": data["collectionName"],
            "blockchain": data["blockchain"]
        }
