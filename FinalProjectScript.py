"""Add a new numeric field to the given table, for each existing record, sum selected fields, and write the value in the newly created field."""

import arcpy

tableName = arcpy.GetParameterAsText(0)
selectedFields = arcpy.GetParameterAsText(1)
newFieldName = arcpy.GetParameterAsText(2)

listOfSelectedFields = selectedFields.split(";")

arcpy.AddMessage("Selected file: " + tableName)
arcpy.AddMessage("Selected fields: " + str(listOfSelectedFields))
arcpy.AddMessage("Output field name: " + newFieldName)

# Define which data types that are valid, ie have numeric values
# The data types are sorted in this order because their
# index is used as a ranking system later
validTypes = ["SmallInteger", "Integer", "Single",  "Double"]

newFieldType = "SmallInteger"

approvedFields = []
listOfFields = arcpy.ListFields(tableName)
for field in listOfFields:
    if field.name in listOfSelectedFields:
        arcpy.AddMessage("Checking field: " + field.name)
        if field.type in validTypes:
            arcpy.AddMessage("Data type OK: " + str(field.type))
            approvedFields.append(field.name)
            # Compare the index of the newfieldtype with the index of the current field
            # If the currently selected type for the new field would be unable to contain
            # the values of the current field update the type for the new field to be the same as the current field
            if validTypes.index(field.type) > validTypes.index(newFieldType):
                newFieldType = field.type
                arcpy.AddMessage("Datatype for the new field is updated to: " + str(newFieldType))
        else:
            arcpy.AddMessage("Invalid field type: " + str(field.type))
            arcpy.AddMessage("Valid types are: " + str(validTypes))

# Inform the user of the data type for the new field and list the fields which will be part of the sum.
arcpy.AddMessage("Datatype for the new field is: " + str(newFieldType))
arcpy.AddMessage("Valid fields are: " + str(approvedFields))

# Create the new field in which the sum will be stored
arcpy.AddField_management(tableName, newFieldName, newFieldType)

# Get a cursor for the table which allows updating the records
records = arcpy.UpdateCursor(tableName)

numberOfUpdatedRecords = 0

for record in records:
    # Initialize the sum to 0
    recordSum = 0
    # Iterate over the approved fields and add the cell value to the sum.
    for fieldName in approvedFields:
        cellValue = record.getValue(fieldName)
        recordSum = recordSum + cellValue
    # Write the sum in the new field
    record.setValue(newFieldName, recordSum)
    # Store updated records in table
    records.updateRow(record)

    numberOfUpdatedRecords = numberOfUpdatedRecords + 1

arcpy.AddMessage("Number of records has been updated: " + str(numberOfUpdatedRecords))
