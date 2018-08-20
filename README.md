# scrapy-learn
for scrapy learn



----

1. projectName :为项目名

`创建一个scrapy项目: scrapy startproject projectName`

----

1. Quotes : spider的名称 
2.  quotes.toscrape.com 爬虫所要爬取的域名地址

`新建spider:scrapy genspider Quotes quotes.toscrape.com` 

---

1. Quotes : spider名称
2. quotes.json ：输出的文件名

`运行spider并将parse结果输出到文件:scrapy crawl Quotes -o quotes.json`

文件名后缀包括:

- json
- jl (json line)
- csv
- marshal
- pickle
- xml







