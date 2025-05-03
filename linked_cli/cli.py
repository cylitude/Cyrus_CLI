# linked_cli/cli.py

import argparse
from linked_cli.data_generator import generate_items
from linked_cli.linked_list    import LinkedList


def main():
    parser = argparse.ArgumentParser(
        prog='python -m linked_cli.cli',
        description='''
Cyrus_CLI

A simple command-line tool to generate, sort, and search
Item objects in an in-memory linked list.
''',
        add_help=False,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    
    general = parser.add_argument_group('General options')
    general.add_argument(
        '-h', '--help',
        action='help',
        help='Show this help message and exit'
    )
    general.add_argument(
        '--seed', '-S',
        type=int,
        metavar='SEED',
        help='Seed RNG for reproducible output'
    )

    # Generate Function
    generation = parser.add_argument_group('Generation')
    generation.add_argument(
        '-g', '--generate',
        type=int,
        metavar='N',
        help='Generate N random items'
    )

    # Sort Function
    sorting = parser.add_argument_group('Sorting')
    sorting.add_argument(
        '-o', '--sort',
        choices=['asc', 'desc'],
        metavar='DIR',
        help='Sort items by date (asc or desc)'
    )

    # Search Function
    searching = parser.add_argument_group('Searching')
    searching.add_argument(
        '-s', '--search',
        metavar='NAME',
        help='Search for an item by name'
    )

    args = parser.parse_args()
    ll = LinkedList()

    
    if args.generate is not None:
        items = generate_items(args.generate, seed=args.seed)
        for item in items:
            ll.append(item)
        print(f"\nGenerated {len(items)} item{'s' if len(items) != 1 else ''}.")

    
    if args.sort:
        ll.sort(ascending=(args.sort == 'asc'))
        ordered = ll.to_list()
        direction = 'ascending' if args.sort == 'asc' else 'descending'
        print(f"\nItems sorted by date ({direction}):")
        for itm in ordered:
            date_str = itm.date.strftime('%Y-%m-%d %H:%M:%S')
            print(f'{{"id": "{itm.id}", "name": "{itm.name}", "date": "{date_str}"}}')

    
    if args.search:
        found = ll.search(args.search)
        print()
        if found:
            print('Retrieved Items:')
            date_str = found.date.strftime('%Y-%m-%d %H:%M:%S')
            print(f'{{"id": "{found.id}", "name": "{found.name}", "date": "{date_str}"}}')
        else:
            print(f"No item named {args.search}")


if __name__ == '__main__':
    main()
