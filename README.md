# Statistic-Lang
package needed:
Flask, scrapy, jsonlines

|-- controller<br>
    &nbsp$nbsp-- predAPI.py                 # start Flask on localhost, port 2222.<br>
   
|-- statlang                      # web crawler using scrapy.<br>
    |-- staglang
        |-- spiders
            -- spider_lang.py     # spider crawl data from github.
         -- middlewares.py        # crawler middlewares
         -- piplines.py           # I/O operations
     -- dbug.py                   # execute crawler

|-- trendModel
    |-- datas                     # datas extracted from json
    |-- models                    # trained models for each languages
     -- createDataset.py          # create dataset.
     -- predService.py            # train models and predict
     
     
