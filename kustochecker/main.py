import clr
import os
from System import Reflection


# Get current path and append location of the DLL 
file_path = f'{os.getcwd()}/Kusto.Language.dll'

# Load the DLL (requires absolute path)
Reflection.Assembly.LoadFile(file_path)

# Import the KustoCode method from Kusto.Language class (loaded via DLL)
from Kusto.Language import KustoCode
from Kusto.Language.Symbols import DatabaseSymbol, TableSymbol 
from Kusto.Language import GlobalState


# Parse the incorrect example KQL query (sorty instead of sort)
example_query = '''SigninLogs
    | where TimeGenerated >= ago(7d)
    | sorty by TimeGenerated, Identity desc
    | take 5'''

## Simple example only performing base KQL syntax checking
code = KustoCode.parse(example_query)

## ParseAndAnalyze example with GlobalState
# Add an incorrect global state (str instead of datetime for TimeGenerated) 
#global_state = GlobalState.Default.WithDatabase(DatabaseSymbol('db', 
#                TableSymbol('SigninLogs', '(TimeGenerated: str, Identity: str')))
#code = KustoCode.ParseAndAnalyze(example_query, global_state)

# Run diagnostics, print issues when there are errors found (ie. count > 0)
diagnostics = code.GetDiagnostics()

if (diagnostics.Count > 0):
    for diag in diagnostics:
        message = {
            'query': example_query,
            'severity': diag.Severity,
            'message': diag.Message,
            'length': diag.Length,
            'start': diag.Start,
            'end': diag.End,
            'troublemaker': example_query[diag.Start:diag.End]
        }
        print(message)

