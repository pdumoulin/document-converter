# document-converter

Wrapper script for [soffice](https://www.systutorials.com/docs/linux/man/1-soffice/) that converts files in place.

## Example
```
$ python run.py /home/mydir/ docx --include-suffix txt
convert /home/mydir/readme.txt -> /home/mydir/readme.docx using filter : MS Word 2007 XML
```

## Help
```
usage: run.py [-h] [-r] [--dry-run] [--exclude-prefix EXCLUDE_PREFIX [EXCLUDE_PREFIX ...]] [--include-suffix INCLUDE_SUFFIX [INCLUDE_SUFFIX ...]] directory output_format

positional arguments:
  directory             directory to search for files in
  output_format         convert to format

optional arguments:
  -h, --help            show this help message and exit
  -r                    recursively search directory (default: False)
  --dry-run             output filenames, do not convert (default: False)
  --exclude-prefix EXCLUDE_PREFIX [EXCLUDE_PREFIX ...]
                        filename prefix(es) to skip (default: ['.', '~'])
  --include-suffix INCLUDE_SUFFIX [INCLUDE_SUFFIX ...]
                        filename suffix(es) to match (default: *)
```
