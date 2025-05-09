import itertools
from openpyxl import Workbook

# Define the class for parameter options
class OrderParameters:
    def __init__(self):
        self.parameters = {
            "Users": {'OWN': 1, 'CLI': 3, 'INST': 5},
            "SMPF": {'ACTIVE': 'active', 'PASSIVE': 'passive'},
            "DQ_Options": {'NULL': 'null', 'DQ': 'dq'},
            "OrderType": {'LIMIT': 2, 'SL_MKT': 3, 'SL_LMT': 4, 'MARKET': 5},
            "TimeInForce": {'DAY': 0, 'GTC': 1, 'IOC': 3, 'GTDt': 6, 'EOS': 7},
            "OrderActions": {'New': 'New', 'Modify': 'Modify', 'Cancel': 'Cancel'},
            "Side": {'BUY': 'buy', 'SELL': 'sell'}
        }

# Class to generate all combinations of parameters
class TestCaseGenerator:
    def __init__(self, parameters: OrderParameters):
        self.parameters = parameters
        self.test_cases = []

    def generate_test_cases(self):
        self.test_cases = []
        # Define the order for test case name generation
        ordered_keys = ['Side', 'Users', 'OrderType', 'TimeInForce', 'SMPF', 'DQ_Options', 'OrderActions']
        param_dict = self.parameters.parameters

        # Generate list of value lists in the fixed order
        list_of_values = [list(param_dict[key].keys()) for key in ordered_keys]

        # Generate all combinations
        for idx, values in enumerate(itertools.product(*list_of_values), start=1):
            # Map each parameter name to its value in the current combination
            param_map = dict(zip(ordered_keys, values))
            # Build the test case name based on the parameter values in order
            name_parts = [str(param_map[param]) for param in ordered_keys]
            test_case_name = "_".join(name_parts)
            # Store the test case details
            self.test_cases.append([str(idx), test_case_name] + list(values))

    def get_test_cases(self):
        return self.test_cases

# Class to export test cases to Excel
class ExcelReporter:
    def __init__(self, filename: str, sheet_name: str = 'Configuration'):
        self.filename = filename
        self.sheet_name = sheet_name

    def export(self, test_cases, headers):
        wb = Workbook()
        ws = wb.active
        ws.title = self.sheet_name

        # Write headers
        ws.append(headers)
        # Write test case rows
        for row in test_cases:
            ws.append(row)

        # Save the workbook
        wb.save(self.filename)
        print(f"Excel file '{self.filename}' generated with {len(test_cases)} test cases.")

# Main class to coordinate the process
class TestCaseManager:
    def __init__(self):
        self.parameters = OrderParameters()
        self.generator = TestCaseGenerator(self.parameters)
        self.exporter = ExcelReporter("ETI_UAT_Algo_Output.xlsx")

    def get_headers(self):
        param_keys = ['Side', 'Users', 'OrderType', 'TimeInForce', 'SMPF', 'DQ_Options', 'OrderActions']
        return ['Sr No', 'Test_case_name'] + param_keys

    def run(self):
        self.generator.generate_test_cases()
        headers = self.get_headers()
        self.exporter.export(self.generator.get_test_cases(), headers)

# Entry point
if __name__ == "__main__":
    manager = TestCaseManager()
    manager.run()