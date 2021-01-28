from redminelib import Redmine


class RedmineEntry(object):
    def __init__(self, url, username, password):
        self.redmine = Redmine(url, username=username, password=password)

    def submitTimeEntry(self, date, ticket_number, logged_time, activity, comment):
        time_entry = self.redmine.time_entry.new()
        time_entry.issue_id = ticket_number
        time_entry.spent_on = date
        # time_entry.hours = 3   # TODO
        time_entry.hours = logged_time
        time_entry.activity_id = activity
        time_entry.comments = comment
        # time_entry.save()

        # TODO : Debug
        print(
            "submit: ",
            ticket_number,
            date,
            logged_time,
            activity,
            comment
        )
