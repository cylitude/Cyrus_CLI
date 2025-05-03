import argparse
from linked_cli.data_generator import generate_items
from linked_cli.linked_list    import LinkedList

def main():
    """
    Entry point for the CLI. Parses command-line arguments into three
    logical groups (general, generation, sorting, searching), then
    invokes the corresponding linked-list operations.
    """
    # Setup argparse with a custom description
    parser = argparse.ArgumentParser(
        prog='python -m linked_cli.cli',              # how users should invoke
        description='''
        
Cyrus_CLI

A simple command-line tool to generate, sort, and search
Item objects in an in-memory linked list.
''',                                             # raw multi-line help text
        add_help=False,                               # we'll add -h/--help manually
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # General Options
    general = parser.add_argument_group('General options')
    general.add_argument(
        '-h', '--help',
        action='help',                               # special action: print help & exit
        help='Show this help message and exit'
    )
    general.add_argument(
        '--seed', '-S',
        type=int,
        metavar='SEED',                              # shows as `--seed SEED`
        help='Seed RNG for reproducible output'
    )

    # Generate Feature
    generation = parser.add_argument_group('Generation')
    generation.add_argument(
        '-g', '--generate',
        type=int,
        metavar='N',
        help='Generate N random items'               # will call generate_items(N, seed)
    )

    # Sort Feature
    sorting = parser.add_argument_group('Sorting')
    sorting.add_argument(
        '-o', '--sort',
        choices=['asc', 'desc'],
        metavar='DIR',                               # shows as `--sort DIR`
        help='Sort items by date (asc or desc)'
    )

    # Search Feature
    searching = parser.add_argument_group('Searching')
    searching.add_argument(
        '-s', '--search',
        metavar='NAME',
        help='Search for an item by name'
    )

    # Parsing everything
    args = parser.parse_args()

    # Instantiate our in-memory linked list
    ll = LinkedList()

    # Handling the Generating process
    if args.generate is not None:
        # generate_items reads seed for deterministic randomness
        items = generate_items(args.generate, seed=args.seed)
        for item in items:
            ll.append(item)                           # O(1) append to tail
        # pluralize "item(s)" correctly
        count = len(items)
        print(f"\nGenerated {count} item{'s' if count != 1 else ''}.")

    # Handling the Sorting process
    if args.sort:
        # ascending flag: True if 'asc'
        ll.sort(ascending=(args.sort == 'asc'))      # merge-sort O(n log n)
        ordered = ll.to_list()                       # flatten for printing
        direction = 'ascending' if args.sort == 'asc' else 'descending'
        print(f"\nItems sorted by date ({direction}):")
        for itm in ordered:
            # human-friendly timestamp format
            date_str = itm.date.strftime('%Y-%m-%d %H:%M:%S')
            # JSON-style output for easy parsing
            print(f'{{"id": "{itm.id}", "name": "{itm.name}", "date": "{date_str}"}}')

    # Handle the Searching process 
    if args.search:
        found = ll.search(args.search)               # O(n) lookup
        print()                                      # blank line for readability
        if found:
            print('Retrieved Items:')
            date_str = found.date.strftime('%Y-%m-%d %H:%M:%S')
            print(f'{{"id": "{found.id}", "name": "{found.name}", "date": "{date_str}"}}')
        else:
            # clear message if no match
            print(f"No item named {args.search}")

if __name__ == '__main__':
    main()
