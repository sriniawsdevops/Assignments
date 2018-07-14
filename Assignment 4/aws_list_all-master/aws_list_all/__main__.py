#!/usr/bin/env python
from __future__ import print_function

import os
from argparse import ArgumentParser

from .introspection import get_listing_operations, get_services, get_verbs
from .query import do_list_files, do_query


def main():
    """Parse CLI arguments to either list services, operations, queries or existing json files"""
    parser = ArgumentParser(
        prog="aws_list_all",
        description=(
            "List AWS resources on one account across regions and services. "
            "Saves result into json files, which can then be passed to this tool again "
            "to list the contents."
        )
    )
    subparsers = parser.add_subparsers(
        description='List of subcommands. Use <subcommand> --help for more parameters',
        dest='command',
        metavar='COMMAND'
    )

    # Query is the main subcommand, so we put it first
    query = subparsers.add_parser('query', description='Query AWS for resources', help='Query AWS for resources')
    query.add_argument(
        '--service', action='append', help='Restrict querying to the given service (can be specified multiple times)'
    )
    query.add_argument(
        '--region', action='append', help='Restrict querying to the given region (can be specified multiple times)'
    )
    query.add_argument(
        '--operation',
        action='append',
        help='Restrict querying to the given operation (can be specified multiple times)'
    )
    query.add_argument('--directory', default='.', help='Directory to save result listings to')

    # Once you have queried, show is the next most important command. So it comes second
    show = subparsers.add_parser(
        'show', description='Show a summary or details of a saved listing', help='Display saved listings'
    )
    show.add_argument('listingfile', nargs='*', help='listing file(s) to load and print')
    show.add_argument('--verbose', action='store_true', help='print given listing files with detailed info')

    # Introspection debugging is not the main function. So we put it all into a subcommand.
    introspect = subparsers.add_parser(
        'introspect',
        description='Print introspection debugging information',
        help='Print introspection debugging information'
    )
    subparsers = introspect.add_subparsers(
        description='Pieces of debug information to collect. Use <DETAIL> --help for more parameters',
        dest='introspect',
        metavar='DETAIL'
    )

    subparsers.add_parser(
        'list-services',
        description='Lists short names of AWS services that the current boto3 version has clients for.',
        help='List available AWS services'
    )
    ops = subparsers.add_parser(
        'list-operations',
        description='List all discovered listing operations on all (or specified) services',
        help='List discovered listing operations'
    )
    ops.add_argument(
        '--service',
        action='append',
        help='Only list discovered operations of the given service (can be specified multiple times)'
    )
    subparsers.add_parser('debug', description='Debug information', help='Debug information')
    args = parser.parse_args()

    if args.command == "query":
        if args.directory:
            try:
                os.makedirs(args.directory)
            except OSError:
                pass
            os.chdir(args.directory)
        services = args.service or get_services()
        do_query(services, args.region, args.operation)
    elif args.command == "show" and args.listingfile:
        do_list_files(args.listingfile, verbose=args.verbose)
    elif args.command == "introspect":
        if args.introspect == "list-services":
            for service in get_services():
                print(service)
        elif args.introspect == "list-operations":
            for service in args.service or get_services():
                for operation in get_listing_operations(service):
                    print(service, operation)
        elif args.introspect == "debug":
            for service in get_services():
                for verb in get_verbs(service):
                    print(service, verb)
        else:
            introspect.print_help()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
