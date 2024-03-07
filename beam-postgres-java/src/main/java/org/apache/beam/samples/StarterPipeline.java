/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.apache.beam.samples;

import org.apache.beam.sdk.Pipeline;
import org.apache.beam.sdk.coders.StringUtf8Coder;
import org.apache.beam.sdk.options.PipelineOptionsFactory;
import org.apache.beam.sdk.options.PipelineOptions;
import org.apache.beam.sdk.values.PCollection;
import org.apache.beam.io.debezium.DebeziumIO;
import org.apache.beam.io.debezium.SourceRecordJson;
import io.debezium.connector.postgresql.PostgresConnector;
import org.apache.beam.io.debezium.KafkaSourceConsumerFn;

import org.apache.beam.io.debezium.KafkaSourceConsumerFn.DebeziumSDFDatabaseHistory;

public class StarterPipeline {
  public static void startDebeziumIOPostgreSql() {
    PipelineOptions options = PipelineOptionsFactory.create();
    Pipeline p = Pipeline.create(options);
    PCollection<String> results =
        p.apply(
            DebeziumIO.<String>read()
                .withConnectorConfiguration(
                    DebeziumIO.ConnectorConfiguration.create()
                        .withUsername("postgres")
                        .withPassword("mysecretpassword")
                        .withConnectorClass(PostgresConnector.class)
                        .withHostName("localhost")
                        .withPort("5432")
                        .withConnectionProperty("database.dbname", "postgres")
                        .withConnectionProperty("database.server.id", "184054")
                        .withConnectionProperty("database.server.name", "dbserver1")
                        .withConnectionProperty("include.schema.changes", "false")
                        .withConnectionProperty("plugin.name", "pgoutput"))
                .withFormatFunction(new SourceRecordJson.SourceRecordJsonMapper())
                .withMaxNumberOfRecords(30)
                .withCoder(StringUtf8Coder.of()));

    p.run().waitUntilFinish();
  }

  public static void main(String[] args) {
    startDebeziumIOPostgreSql();
  }
}
