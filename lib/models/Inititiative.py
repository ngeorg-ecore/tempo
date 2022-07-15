import json

from lib.functions.get_issue import get_issue
from lib.functions.get_issues_by_jql import get_issues_by_jql
from lib.models.guidelines import Column, Model, String


class Initiative(Model):
    # issuetype = initiative and project=CBU and status != Done
    __bind_key__ = "persistency"
    __tablename__ = "initiative"

    issue_key = Column(String)
    linked_epics = Column(String)
    summary = Column(String)
    status = Column(String)

    def get_epics(self):
        try:
            jql = f"issue in linkedIssues('{self.issue_key}')"
            issues = get_issues_by_jql(jql)['issues']
            print("Getting Epics for Issue", self.issue_key)
            print(issues)
            self.update(linked_epics=json.dumps(issues))

        except:
            self.update(linked_epics=json.dumps({}))

    def get_data(self):
        try:
            data = get_issue(self.issue_key)
            self.update(summary=data['fields']['summary'], status=data['fields']['status']['name'])
        except:
            pass

    @property
    def epics(self):
        print(self.linked_epics)
        return json.loads(self.linked_epics)

    def postfunctions(self):
        self.get_data()
        self.get_epics()
