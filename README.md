# crawler

In order to run the project, please run following command:
```
docker run -d -p 80:80 dockergil90/pastebincrawler:1.0
```

After runng the container take a look at the docker logs you'll see the prints of the scraped data 

The structure of the project is as follows:
Setup file calls PasateBinCrawlerJob every 2 minutes
PasteBinCrawlerJob implements JobHandler and it contains the main logic of the crawler

The main logic of the crawler consists of:
1. Getting all public pastes links from pastebin
2. Checking which pastebin links are new and need to be scraped
3. Downloading each and every new paste page
4. Analyzing each page and running a "normalizer" function on it (i.e., normalizing the text as requested)
5. Saving in the db.

Take a look at the github project, available at:
https://github.com/GilGald/PastebinCrawler.git

Docker image location:
https://hub.docker.com/repository/docker/dockergil90/pastebincrawler

* In preparing the project, I took into account working with SOLID and OOP priciples
* There is a scraping API for pastebin, but as this would be easier to implement, I refrained from using it
* I completed all 3 bonuses
* Database located in db.json with tinydb

* I took some scalability considirations while working on this project,
but there might be some places that would need futher refactroing


![GitHub Logo](https://images.pexels.com/photos/997313/pexels-photo-997313.jpeg?auto=compress&cs=tinysrgb&dpr=3&h=750&w=1260)
