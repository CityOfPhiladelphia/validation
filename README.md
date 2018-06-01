This is a script meant to validate tables, specifically .csv files for now, according to a mix of table schema and custom constraints. The script is called in the form of "valitool.py *.csv *.json"

In terms of table schema, the format is near identical to that of https://frictionlessdata.io/specs/table-schema/. Please refer to there for the basics of schema.

The modifications done to table schema for the purposes of this validation are few and meant for use specifically with a few fields. In the constraints field, an additional "custom" field can be added.

This "custom" field can be used with, currently, one of a few different constraints. "phil_zip" locks the field into only being valid if all of the zip codes present reside in Philadelphia. "phil_tract" operates much the same way, but in terms of Census Tracts. "lat" and "lon" are sanity checks, as rather than using geodata to determine if the exact coordinates are inside the city, it just checks to make sure that they are within some reasonable range to be in and around the city, to make sure for example, that the two specifications aren't swapped around.

Currently, the errors are pushed to a csv file, bearing the name of the original csv, plus "_error_dump". This csv is emailed to the address located in the "owner" field that should be place at the top of the schema. The email sent from should be specified as environment variables, VALI_EMAIL and VALI_PW.

Examples of the schemas in use can be found in the "EXAMPLES" folder.
