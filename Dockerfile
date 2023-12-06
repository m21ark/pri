FROM solr:latest

COPY . /home/

COPY solr/startup.sh /home/solr/startup.sh

ENTRYPOINT ["/home/solr/startup.sh"]
