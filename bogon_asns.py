#!/usr/bin/env python3
''' Find bogon ASNs in BGP full feed '''

import sys
import fileinput
from pathlib import Path
from flashtext import KeywordProcessor

def main():
    ''' Main function '''

    if len(sys.argv) == 2:
        if Path(sys.argv[1]).is_file():

            kwd_proc = KeywordProcessor()

            # RFC 4893 AS_TRANS, RFC 7300 Last 16 bit ASN, RFC 7300 Last 32 bit ASN
            kwd_proc.add_keywords_from_list(['23456', '65535', '4294967295'])
            # RFC 5398 and documentation/example ASNs
            kwd_proc.add_keywords_from_list([str(i) for i in range(64496, 64511)])
            # RFC 6996 Private ASNs
            kwd_proc.add_keywords_from_list([str(i) for i in range(64512, 65534)])
            # RFC 5398 and documentation/example ASNs
            kwd_proc.add_keywords_from_list([str(i) for i in range(65536, 65551)])
            # RFC IANA reserved ASNs
            kwd_proc.add_keywords_from_list([str(i) for i in range(65552, 131071)])
            # RFC 6996 Private ASNs
            # WARNING: Disabled to avoid RAM exhaustion
            # kwd_proc.add_keywords_from_list([str(i) for i in range(4200000000, 4294967294)])

            for as_path_record in fileinput.input(sys.argv[1], encoding="utf-8"):
                as_path = as_path_record.rstrip()
                bogon_asn = kwd_proc.extract_keywords(as_path_record)
                if bogon_asn:
                    print(f"{', '.join(map(str, bogon_asn))}|{as_path}")

        else:
            print (f'[!] File {sys.argv[1]} does not exist')
            sys.exit(1)
    else:
        print ('[!] Please provide a file path as an argument')
        sys.exit(1)


if __name__ == '__main__':
    main()
