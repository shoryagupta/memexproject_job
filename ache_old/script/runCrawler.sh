#!/bin/sh
cd .;
java -Xmx32g -cp class focusedCrawler.crawler.CrawlerManager conf/crawler/crawler.cfg > log/crawler.log 2>&1 &
