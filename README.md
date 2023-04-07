# StegTool
A command line steganograpghy tool to hide messages within audio and image files.

![alt text](https://github.com/rmcmillan34/StegTool/blob/main/encoded/steg_logo.png?raw=true)

## TODO
[ ] - Complete README documentation
[x] - Implement Verbose output


## Installation

Use git clone to install the latest version of StegTool.

```bash
git clone https://github.com/rmcmillan34/StegTool.git
```

### Requirements
StegTool was written in Python 3.9.7. This version of Python is the recommended minimum, however I believe it will work on any Python 3 installation.

The following modules are required to run this software:

- argparse
- cv2
- os
- system

## Usage
StegTool is a command line tool written in python
```sh
usage: StegTool [-h] [-e] [-d] [-v] filename message

A comand line tool to encode a secret message within an image file.

positional arguments:
  filename       name of file to perform steganographic function on
  message        Text string of message to be encoded

optional arguments:
  -h, --help     show this help message and exit
  -e, --encode   Performs steganographic encode function
  -d, --decode   Performs steganographic decode function
  -v, --verbose  Enables a verbose output. Program will output what it is doing.
```

## Contributing

Pull requests will be welcome after 30th April 2023. For major changes, please open an issue first 
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[GNU GPL v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html)
