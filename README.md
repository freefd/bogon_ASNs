# How to find bogon ASNs in the Internet

This is a simple PoC how to find bogon ASNs in the Internet without any network equipment and real BGP full feed.

## Installation

### BGP Scanner
#### Installing from packages
Install [bgpscanner](https://www.isolario.it/web_content/php/site_content/tools.php)<sup id="a1">[1](#f1)</sup> tool using deb packages:
```bash
$ wget https://www.isolario.it/tools/libisocore1_1.0-1_20190212_amd64.deb https://www.isolario.it/tools/bgpscanner_1.0-1_20190212_amd64.deb
$ sudo dpkg -i libisocore1_1.0-1_20190212_amd64.deb bgpscanner_1.0-1_20190212_amd64.deb
```
#### Building from source
:warning: TODO

### RIS Raw Data
Download a latest [RIS Raw Data](http://data.ris.ripe.net/rrc00/)<sup id="a2">[2](#f2)</sup> snapshot:
```bash
$ wget http://data.ris.ripe.net/rrc00/latest-bview.gz
```

### FlashText
Install the flashtext<sup id="a3">[3](#f3)</sup> python's module implementation<sup id="a4">[4](#f4)</sup>:
```bash
$ sudo pip3 install flashtext
```
## Usage
Run the command to extract and save RIS Raw Data to a text file named "bogons":
```bash
$ bgpscanner latest-bview.gz | awk -F'|' '{print $3"|"$2}' | sort -V | uniq > bogons
```
The output should be similar as follows:
```
396503 32097 33387 42615|185.186.8.0/24
396503 32097 33387 44421|185.234.214.0/24
396503 32097 33387 64236 17019|66.85.92.0/22
```

Run the python script to find out whether any bogon ASNs in the file "bogons" that was previously saved:
```bash
python3 scripts/bogon_asns.py bogons
```
The first argument must be a relative or an absolute path to the file.

The example output:
```
65225|3333 1103 9498 55410 55410 38266 65225|2402:3a80:ca0::/43
65542, 65542|3333 1103 9498 132717 132717 65542 65542 134279|103.197.121.0/24
64646, 65001, 65083|3333 1103 30844 327693 37611 {16637,64646,65001,65083}|169.0.0.0/15
64555|3333 1103 58453 45899 45899 45899 45899 {16625,64555}|2001:ee0:3200::/40
65817|3333 1136 9498 703 65817|202.75.201.0/24
```

Where the format is:
```
bogon ASN(s)|as-path|prefix(es)
```

However, you can define filter(s) to extract only records you need:
```bash
$ bgpscanner -p ' 55410 ' latest-bview.gz | awk -F'|' '{print $3"|"$2}' | sort -V | uniq > bogons
```
The example above will return only records contained AS55410 in AS path. More information about filtering you can find at the References below<sup id="a5">[5](#f5)</sup>.

## References
<b id="f1">1</b>. BGP Scanner: https://gitlab.com/Isolario/bgpscanner [↩](#a1)<br/>
<b id="f2">2</b>. RIS Raw Data: https://www.ripe.net/analyse/internet-measurements/routing-information-service-ris/ris-raw-data [↩](#a2)<br/>
<b id="f3">3</b>. FlashText algorithm: https://arxiv.org/pdf/1711.00046.pdf [↩](#a3)<br/>
<b id="f4">4</b>. FlashText python module documentation: https://flashtext.readthedocs.io/en/latest/ [↩](#a4)<br/>
<b id="f5">5</b>. About bgpscanner filtering options: [↩](#a5)
* https://gitlab.com/Isolario/bgpscanner/wikis/Home#filtering
* https://ripe77.ripe.net/presentations/12-pres.pdf#page=20 (page 20)
