# StegTool
A command line steganograpghy tool to hide messages within audio and image files.

![alt text](https://github.com/rmcmillan34/StegTool/blob/main/encoded/steg_logo.png?raw=true)

## TODO
[ ] - Complete README documentation
[ ] - Implement Verbose output
[ ] - Secret message encryption/password protection
[ ] - Graphical User Interface


## Installation

Use git clone to install the latest version of StegTool.

```bash
git clone https://github.com/rmcmillan34/StegTool.git
```

## Usage

```sh
# Encode a secret message into a carrier file.
python3 StegTool.py IMAGENAME.jpg --encode SECRETMESSAGE

# Decode a carrier file
python3 StegTool.py IMAGENAME.jpg --decode

# Enable verbose output.
python3 StegTool.py IMAGENAME.jpg --encode --verbose
```

## Contributing

Pull requests will be welcome after 30th April 2023. For major changes, please open an issue first 
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[GNU GPL v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html)
