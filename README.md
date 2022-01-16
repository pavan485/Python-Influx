# Python-InfluxDB

InfluxDB works really well with observability tools like Grafana and more. For scenarios where an observability tool cannot be connected using API and only works with DB's, we can use this integration to pull timeseries data from Catchpoint and store it in influxDB so that we can plot similar dashboards as Catchpoint.

# Prerequisites

1. Python v3.x
3. InfluxDB v2.x
4. Catchpoint account with a REST API consumer

# Installation and Configuration

Copy the Python-Influx folder to your machine
Run following commands in the directory /Python-Influx
   - python -m pip install requests
   - pip install pyyaml
   - pip install logger
   - pip install influxdb-client
   
   
### Configuration
In the config.yaml file under config sub-directory, enter your Catchpoint API consumer key and secret
In the tests object of the config_catchpoint.py file, enter the test IDs you want to pull the data for in a dictionary of array format.

*Example:*

    test_ids: { 
              web : ['142619','142620','142621','142622'],
              traceroute : ['142607','142608','142609'], 
              api : ['142637','142638','142683','142689'],
              transaction: ['142602','142603'],
              dns : '142644','142645','142646','142647'],
              smtp : ['142604'],
              websocket: ['842700'],
              ping : ['142599','142600','142601']
              
          }
---       
In the config_influx.py file, enter your Influx API token.
In the same influx_config.yaml file, enter your InfluxDB organization name, bucket name, url and measurement name where the data will be stored. Please note that the organization and bucket should be created after installation of InfluxDB. The default Influx URL is http://localhost:8086


### How to run

 
- Create a cronjob to run the application.py file every 15 minutes.

*Example crontab entry, if the file resides in /usr/local/bin/application.py*

`*/15 * * * * cd /usr/local/bin/ && python /usr/local/bin/application.py > /usr/local/bin/logs/cronlog.log 2>&1`


## File Structure

    Python-Influx/
    ├── request_handler.py          ## Contains APIs related to authentication       
    ├── config
    | ├── config_catchpoint.yaml    ## Configuration file for Catchpoint 
    | ├── config_influx.yaml        ## Configuration file for InfluxDB 
    ├── log
    | ├── app.log                   ## Contains informational and error logs. 
    ├── application.py              ## main file
    ├── log.py
    ├── request_handler.py          ## Contains API requests for token and raw endpoint 
    ├── utils.py                    ##  utility fot partsing data, inserting it to influx and validating configurations
           

Once the script starts running and data is inserted into InfluxDB, it can queried using [Flux queries](https://docs.influxdata.com/influxdb/v2.1/query-data/execute-queries/influx-api/) or visualized in graphs by opening the [Influx Data Explorer](https://docs.influxdata.com/influxdb/cloud/query-data/execute-queries/data-explorer/). 

