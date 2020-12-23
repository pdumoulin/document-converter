"""Wrapper for soffice CLI to convert files in place."""

import argparse
import os
import subprocess


def main():
    """Entrypoint."""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        'directory',
        help='directory to search for files in'
    )
    parser.add_argument(
        'output_format',
        help='convert to format'
    )
    parser.add_argument(
        '-r',
        action='store_true',
        help='recursively search directory'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='output filenames, do not convert'
    )
    parser.add_argument(
        '--exclude-prefix',
        nargs='+',
        default=['.', '~'],
        help='filename prefix(es) to skip'
    )
    parser.add_argument(
        '--include-suffix',
        nargs='+',
        default='*',
        help='filename suffix(es) to match'
    )

    args = parser.parse_args()

    # check soffice install
    if not args.dry_run and not _check_bin():
        exit('Error: LibreOffice not installed')

    # verify input dir
    if not os.path.isdir(args.directory):
        exit(f'Error: Unable to find directory "{args.directory}"')

    # get all files in directory
    files = []
    if args.r:
        for dirpath, _, filenames in os.walk(args.directory):
            for filename in filenames:
                files.append((dirpath, filename))
    else:
        for filename in os.listdir(args.directory):
            if os.path.isfile(os.path.join(args.directory, filename)):
                files.append((args.directory, filename))

    # filter files by suffix and prefix
    files = [
        x
        for x in files
        if _allow_file(
                x[1],
                args.include_suffix,
                args.exclude_prefix
            )
        ]

    # process files
    for dirpath, filename in files:
        if args.dry_run:
            print(os.path.join(dirpath, filename))
        else:
            _convert_file(
                dirpath,
                filename,
                args.output_format
            )


def _allow_file(filename, include_suffix, exclude_prefix):
    if include_suffix == '*' or any([filename.endswith(x) for x in include_suffix]):  # noqa:E501
        if all(
            [
                not os.path.split(filename)[-1].startswith(y)
                for y in exclude_prefix
            ]
        ):
            return True
    return False


def _convert_file(dirpath, filename, output_format):
    full_path = os.path.join(dirpath, filename)
    subprocess.call([
        'soffice',
        '--headless',
        '--convert-to',
        output_format,
        '--outdir',
        dirpath,
        full_path
    ])


def _check_bin():
    try:
        subprocess.call([
            'soffice',
            '--version'
        ])
    except:  # noqa:E722
        return False
    return True


if __name__ == '__main__':
    main()
