# Digikey-Inventree-Integration

## Setup

`pip install -r requirements.txt`

Put a config.ini file in `inventree_digikey/`

config.ini has the following template

```
[DIGIKEY_API]
CLIENT_ID=
CLIENT_SECRET=

[INVENTREE_API]
URL=<URL to the inventree instance>
USER=
PASSWORD=

# Controls if we import the HTSUS Codes from DK
[SETTINGS]
IMPORT_HTSUS=True

# Controls how DK part categories are mapped to Inventree Catagories, if the 
# imported part's categories is in this list then it will be automapped, if not
# the user will be prompted to select the category.  It is currently assumed that 
# these Inventree Categories already exist.
# <DK_CAT>:<INV_CAT>
[CAEGORIES]
Resistors:Resistors
Capacitors:Capacitors
Transistors:Transistors

# Control what part paramaters to try and import from DK, if the DK Param exists of a part it will be added to the Invetree Parts as the mapped paramater template.  We again assume that these parameter tempaltes already exists.  
[PARAMETERS]
Resistance:Resistance
Tolerance:Tolerance
Power (Watts):Power
Package / Case:Package
Voltage - Rated:Voltage
Capacitance:Capacitance
```