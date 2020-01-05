from servercheck.http import ping_servers
import click
import json
import sys

@click.command()
@click.option("--filename", "-f", default=None)
@click.option("--server", "-s", default=None, multiple=True)
def cli(filename=None, server=None):
    if not filename and not server:
        raise click.UsageError("must provide a JSON file or servers")
    
    # create a ser of servers to prevent duplicates
    servers = set()

    # if --filename or -f option is used then attempy to open file before
    # making requests
    if filename:
        try:
            with open(filename) as f:
                json_servers = json.load(f)
                for s in json_servers:
                    servers.add(s)
        except:
            print("Error: Unable to open or read JSON file")
            sys.exit(1)
    
    if server:
        for s in server:
            servers.add(s)

    results = ping_servers(servers)

    print("Successful Connections")
    print("----------------------")
    for server in results["success"]:
        print(server)
    
    print("\nFailed Connections")
    print("----------------------")
    for server in results["failure"]:
        print(server)

if __name__ == "__main__":
    cli()
