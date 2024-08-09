import argparse
import logging
import re

import apache_beam as beam
from apache_beam.io import ReadFromText
from apache_beam.io import WriteToText
from apache_beam.runners.interactive.caching.streaming_cache import StreamingCacheSink
from apache_beam.io.debezium import ReadFromDebezium
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions
# from apache_beam.transforms.core import WindowInto
from apache_beam import window
from apache_beam.transforms.window import FixedWindows
from apache_beam.transforms.trigger import AfterProcessingTime, AccumulationMode, AfterWatermark
from apache_beam.io import WriteToAvro

from apache_beam.io.debezium import DriverClassName


def run(argv=None, save_main_session=True):
    """Main entry point; defines and runs the wordcount pipeline."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--username',
        dest='username',
        required=True,
        help='Output file to write results to.')
    parser.add_argument(
        '--password',
        dest='password',
        required=True,
        help='Output file to write results to.')
    parser.add_argument(
        '--host',
        dest='host',
        required=True,
        help='Output file to write results to.')
    parser.add_argument(
        '--port',
        dest='port',
        required=True,
        help='Output file to write results to.')
    parser.add_argument(
        '--output',
        dest='output',
        required=True,
        help='Output file to write results to.')
    known_args, pipeline_args = parser.parse_known_args(argv)

    # We use the save_main_session option because one or more DoFn's in this
    # workflow rely on global context (e.g., a module imported at module level).
    pipeline_options = PipelineOptions(pipeline_args)
    pipeline_options.view_as(SetupOptions).save_main_session = save_main_session

    schema = {'fields': {'name': 'key', 'type': 'string'},{'name': 'value', 'type':'string'},}
    

    # The pipeline will be run on exiting the with block.
    with beam.Pipeline(options=pipeline_options) as p:
        p.not_use_test_runner_api = True
        produce = ( 
            p | 'Read' >> ReadFromDebezium(
                connector_class=DriverClassName.POSTGRESQL,
                username="postgres",
                password="mysecretpassword",
                host="localhost",
                port="5432",
                connection_properties = [
                    "database.port=5432",
                    "database.dbname=postgres",
                    "database.server.name=dbserver1",
                    "database.include.list=public",
                    "include.schema.changes=false",
                    "plugin.name=pgoutput",
                ]
            )
            | 'window' >> beam.WindowInto(
                            FixedWindows(1 * 60),
                            trigger=AfterProcessingTime(1 * 60),
                            accumulation_mode=AccumulationMode.DISCARDING,
                            allowed_lateness=1800)
            | WriteToAvro(known_args.output,schema, file_name_suffix='.avro')
        )

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    logging.info("Running")
    run()