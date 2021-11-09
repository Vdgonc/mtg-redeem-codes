import csv
import browser
from browser import Browser
from utils import Config


class BrowserOperator:
    def __init__(self, file_name) -> None:
        self.config = Config(file_name)
        self.browser = Browser()
        self.results = []

    def reedem_batch(self, code_list):
        username = self.config["username"]
        password = self.config["password"]

        self.browser.login(username, password)
        for code in code_list:
            if self.browser.redeem_code(code):
                print("Successfully reedemed code: " + code)
                self.results.append(dict(code=code, status="success"))
            else:
                print("Failed to reedem code: " + code)
                self.results.append(dict(code=code, status="failed"))

    def export_results(self, output_file):
        with open(output_file, "w") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=["code", "status"])
            writer.writeheader()
            for result in self.results:
                writer.writerow(result)

        self.browser.close_browser()  
