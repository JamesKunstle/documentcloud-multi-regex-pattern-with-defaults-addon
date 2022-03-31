"""
This is an add-on to search a document for a regex and output all of the matches
"""

import csv
import re

from documentcloud.addon import AddOn


class Regex(AddOn):
    def main(self):
        if not self.documents:
            self.set_message("Please select at least one document")
            return

        # assumes that the regex pattern list is at least of length 1
        if(len(self.data["regex"]) < 1):
            self.set_message("Please provide at least one regular expression.")
            return
        
        with open("matches.csv", "w+") as file_:

            writer = csv.writer(file_)
            writer.writerow(["pattern", "match", "url"])

            # for each pattern supplied
            for regex_pattern in self.data["regex"]:
                print("Pattern: " + regex_pattern)
                pattern = re.compile(regex_pattern)

                for document in self.client.documents.list(id__in=self.documents):
                    writer.writerows(
                        [regex_pattern, m, document.canonical_url]
                        for m in pattern.findall(document.full_text)
                    )
                    
            print("CSV Document Contents:")
            # go to the beginning of the file
            file_.seek(0)
            # print the file contents
            print(file_.read())

            self.upload_file(file_)


if __name__ == "__main__":
    Regex().main()
