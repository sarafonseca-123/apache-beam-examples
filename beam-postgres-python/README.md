poetry use python3.11

poetry shell
pip install "apache-beam[gcp]" 
Porque não funciona no poetry?

python3 -m apache_beam.examples.wordcount --input texto.txt  --output counts.txt


docker run --name some-postgres -p 5432:5432 -e POSTGRES_PASSWORD=mysecretpassword -d postgres

dentro do container: psql ALTER SYSTEM SET wal_level = logical;
restart container

https://stackoverflow.com/questions/67490668/changing-wal-level-on-postgresql-13-via-client-session-is-not-being-respecte

Na UI, conectado com o DBEAVER:
CREATE TABLE accounts (user_id VARCHAR (50));
INSERT INTO accounts("user_id") VALUES ('sara');




python3 beam_postgres_python/postgres_to_gcs.py \
--username=postgres, \
--password=mysecretpassword, \
--host=localhost, \
--port=5432, \
--output tentativa_1





```
ValueError: Unable to get filesystem from specified path, please use the correct path or ensure the required dependency is installed, e.g., pip3 install "apache-beam[gcp]". Path specified: https://repo.maven.apache.org/maven2/org/apache/beam/beam-sdks-java-io-debezium-expansion-service/2.58.0/beam-sdks-java-io-debezium-expansion-service-2.58.0.jar
```
Erro acima porque o python 11 tá bichado na minha máquina
poetry use python3.9 
poetry shell
sdk install java 21.0.4-tem

python3 beam_postgres_python/postgres_to_gcs.py \
--username=postgres, \
--password=mysecretpassword, \
--host=localhost, \
--port=5432, \
--output tentativa_1
--allow_unsafe_triggers

```
raise ValueError(
ValueError: GroupByKey cannot be applied to an unbounded PCollection with global windowing and a default trigger
```


Tentativa de correção: 

- pipeline_options.view_as(StandardOptions).streaming = True
   - Não funcionou

https://www.waitingforcode.com/apache-beam/triggers-apache-beam/read#:%7E:text=Apache%20Beam%20comes%20with%204,on%20element%27s%20event%20time%20property.&text=processing%20time%20%2D%20this%20trigger%20is,value%20of%20processing%20time%20watermark
https://stackoverflow.com/questions/67539285/what-is-the-default-behavior-of-the-global-window-for-unbounded-pcollections-in


Adicionar windowing e trigger

Windowing: 
https://beam.apache.org/documentation/programming-guide/#windowing

Trigger:
https://beam.apache.org/documentation/programming-guide/#setting-a-trigger

Onde o GroupByKey tá sendo definido?




Caused by: org.postgresql.util.PSQLException: ERROR: logical decoding requires wal_level >= logical:


