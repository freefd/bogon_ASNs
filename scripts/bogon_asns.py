#!/usr/bin/env python3

import sys
import pathlib
from flashtext import KeywordProcessor

def main():
    if pathlib.Path(sys.argv[1]).exists() and pathlib.Path(sys.argv[1]).is_file():
        as_paths_file = open(sys.argv[1], 'r')
    else:
        print ('[!] The file ' + sys.argv[1] + ' was not found')
        exit(1)

    keyword_processor = KeywordProcessor()

    # RFC 4893 AS_TRANS, RFC 7300 Last 16 bit ASN, RFC 7300 Last 32 bit ASN
    keyword_processor.add_keywords_from_list(['23456', '65535', '4294967295'])
    # RFC 5398 and documentation/example ASNs
    keyword_processor.add_keywords_from_list(list([str(i) for i in range(64496, 64511)]))
    # RFC 6996 Private ASNs
    keyword_processor.add_keywords_from_list(list([str(i) for i in range(64512, 65534)]))
    # RFC 5398 and documentation/example ASNs
    keyword_processor.add_keywords_from_list(list([str(i) for i in range(65536, 65551)]))
    # RFC IANA reserved ASNs
    keyword_processor.add_keywords_from_list(list([str(i) for i in range(65552, 131071)]))
    # RFC 6996 Private ASNs, disabled to avoid RAM exhausted
    # keyword_processor.add_keywords_from_list(list([str(i) for i in range(4200000000, 4294967294)]))

    as_paths = [line.rstrip() for line in as_paths_file]

    for as_path in as_paths:
        bogonASN = ''
        bogonASN = keyword_processor.extract_keywords(as_path)
        if bogonASN: print(', '.join(map(str, bogonASN)) + '|' + as_path)

if __name__ == '__main__':
    main()