import clr
import os
from System import Reflection

# Get current path and append location of the DLL 
file_path = f'{os.getcwd()}/Kusto.Language.dll'

# Load the DLL (requires absolute path)
Reflection.Assembly.LoadFile(file_path)

# Import the KustoCode function from Kusto.Language class (loaded via DLL)
from Kusto.Language import KustoCode

# Parse the incorrect KQL query
code = KustoCode.Parse('randomTable| bla')

# Run diagnostics, print issues when there are errors found (ie. count > 0)
diagnostics = code.GetDiagnostics()
if (diagnostics.Count > 0):
    for diag in diagnostics:
        message = {
            'severity': diag.Severity,
            'message': diag.Message,
            'length': diag.Length,
            'start': diag.Start,
            'end': diag.End
        }
        print(message)

