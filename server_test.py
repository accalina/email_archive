# -----------------------------------------------+
# FLASK MAIN SERVER                              +
# -----------------------------------------------+

# IMPORT ----------------------------------------+
from server import app
import unittest

# CLASS -----------------------------------------+
class ServerTestCase(unittest.TestCase):
    
    # Index Testcase ----------------------------+
    # Ensure the Index endpoint is accessable
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/index')
        self.assertEqual(response.status_code, 200)

    # Ensure the template is loaded correctly
    def test_index_templateLoad(self):
        tester = app.test_client(self)
        response = tester.get('/index')
        self.assertTrue(b'Simple Dashboard' in response.data)

    # Ensure the data table is loaded with values
    def test_index_tableLoad(self):
        tester = app.test_client(self)
        response = tester.get('/index')
        self.assertTrue(b'<td>' in response.data)


    # Save Emails Testcase ----------------------------+
    # Ensure the Save Emails endpoint is accessable
    def test_save_emails(self):
        tester = app.test_client(self)
        response = tester.get('/save_emails')
        self.assertEqual(response.status_code, 405) # Should block GET request

    # Send Correct Data to Save Email Endpoint
    def test_save_emails_correctData(self):
        tester = app.test_client(self)
        response = tester.post('/save_emails', data={'event_id': 901, 'email_subject': 'unit testing', 'email_content': 'unit testing'}, follow_redirects = True)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(b'Success' in response.data)
        
    # Send not Integer data as Event ID
    def test_save_emails_notInteger(self):
        tester = app.test_client(self)
        response = tester.post('/save_emails', data={'event_id': 'test99', 'email_subject': 'unit testing', 'email_content': 'Testing Content'}, follow_redirects=True)
        self.assertEqual(response.status_code, 400)
        self.assertTrue(b'Error: EventID must be Integer' in response.data)

    # Send Empty Data data on Email Subject
    def test_save_emails_emptySubject(self):
        tester = app.test_client(self)
        response = tester.post('/save_emails', data={'event_id': 902, 'email_subject': '', 'email_content': 'unit testing'}, follow_redirects=True)
        self.assertEqual(response.status_code, 400)
        self.assertTrue(b'Error: Required Data not provided' in response.data)

    # Send Empty Data data on Email Content
    def test_save_emails_emptySubject(self):
        tester = app.test_client(self)
        response = tester.post('/save_emails', data={'event_id': 903, 'email_subject': 'unit testing', 'email_content': ''}, follow_redirects=True)
        self.assertEqual(response.status_code, 400)
        self.assertTrue(b'Error: Required Data not provided' in response.data)        


    # API Testcase ----------------------------+
    # Ensure the API endpoint is accessable
    def test_api(self):
        tester = app.test_client(self)
        response = tester.get('/api', content_type="text/json")
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
