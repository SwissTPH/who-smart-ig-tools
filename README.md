# who-smart-ig-tools


# Anthro

Reads WHO/anthro github data an create CQL and FHIR Library

 mappinmg with WHO file name

 WHO file name : human readable name : 2nd dimension

"lenanthro":"Lenght" : age
"weianthro":"Weight" : age
"bmianthro":"BMI" : age
"hcanthro":"HeadCircumference" : age
"acanthro":"ArmCircumference" : age
"tsanthro":"tricepsSkinfold" : age
"ssanthro":"subscapularSkinfold" : age
"wfhanthro":"WeightForHeight" : height
"wflanthro":"WeightForLength": length

## Functions

every library come with 

generateZScore{0}(weight  Decimal) -> zScore Decimal
generate{0}From{1}(zscore  Decimal) ->  2nd dimension Decimal
Zscore{0}tables -> List of the zscore table values

where:
- {0} is the human readable name
- {1} is the second dimesion

# configuration

save you configuration in this file anthro/config.py


GITHUB_TOKEN=""
OUTPUT_PATH="/input/"
CANNONICAL_BASE="your_cannonical_base"
FHIR_VERSION="4.0.1"
LIB_VERSION="0.99.99"
INCLUDE_TEST=True

