import click
import json
import sys

from typing import TextIO
from .http import assault
from .stats import Results


@click.command()
@click.option("--requests", "-r", default=500, help="Number of requests")
@click.option("--concurrency", "-c", default=1, help="Number of concurrent requests")
@click.option("--json-file", "-j", default=None, help="Path to output JSON file")
@click.argument("url")
def cli(requests=0, concurrency=0, json_file=None, url=None):
    output_file = None
    if json_file:
        try:
            output_file = open(json_file, "w")
        except:
            print(f"Unable to open file {json_file}")
            sys.exit(1)

    total_time, requests_dicts = assault(url, requests, concurrency)
    results = Results(total_time, requests_dicts)
    display(results, output_file)


def display(results: Results, json_file: TextIO):
    if json_file:
        # Write to the file
        json.dump(
            {
                "successful_requests": results.successful_requests(),
                "slowest": results.slowest(),
                "fastest": results.fastest(),
                "total_time": results.total_time,
                "request_per_minute": results.requests_per_minute(),
                "request_per_second": results.requests_per_second(),
            },
            json_file,
        )
        json_file.close()
        print(".... Done!")
    else:
        # Print to screen
        print(".... Done!")
        print("--- Results ---")
        print(f"Successful requests\t{results.successful_requests()}")
        print(f"Slowest            \t{results.slowest()}")
        print(f"Fastest            \t{results.fastest()}")
        print(f"Total time         \t{results.total_time}")
        print(f"Requests per minute\t{results.requests_per_minute()}")
        print(f"Requests per second\t{results.requests_per_second()}")


if __name__ == "__main__":
    cli()

