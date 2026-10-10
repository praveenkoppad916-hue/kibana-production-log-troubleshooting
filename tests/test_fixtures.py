import json
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
ROWS = [json.loads(line) for line in (ROOT/'data/payment_logs.ndjson').read_text().splitlines() if line.strip()]

class TestSampleLogs(unittest.TestCase):
    def test_transaction_trace(self):
        rows = [r for r in ROWS if r['transaction_id']=='TXN-100245']
        self.assertEqual(len(rows),4)
        self.assertEqual(sum(r['log.level']=='ERROR' for r in rows),2)
        self.assertEqual({r['trace.id'] for r in rows},{'TRACE-A1'})
    def test_status_counts(self):
        self.assertEqual(sum(500<=r['http.response.status_code']<600 for r in ROWS),7)
        self.assertEqual(sum(r['http.response.status_code']==504 for r in ROWS),2)
        self.assertEqual(sum(r['http.response.status_code'] in (401,403) for r in ROWS),2)
    def test_gateway_spike(self):
        self.assertEqual(sum(r['service.name']=='api-gateway' and r['log.level']=='ERROR' for r in ROWS),3)
    def test_queries_are_valid_json(self):
        for file in (ROOT/'queries/elasticsearch').glob('*.json'):
            with self.subTest(file=file.name):
                self.assertIn('query',json.loads(file.read_text()))
if __name__ == '__main__':
    unittest.main()
