from lib.functions.get_issues_by_jql import get_issues_by_jql

jql = "issueType = Initiative and Status != Done"
issues = get_issues_by_jql(jql)

print(issues)