# PBCOperationSpider
* <strong>EN:People's Bank of China open-market operation Spider, using Scrapy to crawl data and Django ORM to store data to database(Mysql used).
* <strong>CN:</strong>中国人民银行公开市场操作记录,使用Scrapy爬取数据，使用Django ORM模型存储数据.

### <strong>Requrements</strong>
* The Project using [Scrapy](https://github.com/scrapy/scrapy) to crawl the web, and using [scrapy-splash](https://github.com/scrapy-plugins/scrapy-splash) to JavaScript integration.
* First, we install all the dependence.

    ``` 
    pip install -r requirements.txt
    ```
* After that, we start a docker container to run splash.

    ```
    docker pull scrapinghub/splash
    docker run -p 8050:8050 scrapinghub/splash
    ```

### <strong>Install And Run</strong>

* Then, we config and create database, In bank/settings.py we can config the database DATABASES option, more details search django document.
We create database and tables with these commands below.

    ```
    ./manage.py dbshell
    > create database bank use default charset utf8;
    > quit
    ./manage.py makemigrations
    ./manage.py migrate
    ``` 

* Then we can run the spider directly

    ```
    cd bank_spider
    scrapy crawl url_spider
    scrapy crawl operation_spider
    ```
* Or we can run it with celery, which will run the spider automatic at a specific time. Redis is as the broker between celery task and worker, before that we must install Redis.
These three commands must run at three different terminals

    ```
    redis-server
    celery -A bank beat -l info
    celery -A bank worker -l info
    ```
It's Ok. Congratulations.
