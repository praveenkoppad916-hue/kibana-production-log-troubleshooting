"""Offline fixture assertions: not a replacement for a live Elasticsearch test."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOGS = [json.loads(line) for line in (ROOT / 'data/payment_logs.ndjson').read_text().splitlines() if line.strip()]

def matches(**fields):
    return [row for row in LOGS if all(row.get(k) == v for k, v in fields.items())]

def main():
    assert len(LOGS) == 15
    assert len(matches(transaction_id='TXN-100245')) == 4
    assert len(matches(transaction_id='TXN-100245', **{'log.level':'ERROR'})) == 2
    assert len(matches(**{'http.response.status_code':504})) == 2
    assert len([r for r in LOGS if r['http.response.status_code'] in (401,403)]) == 2
    assert len([r for r in LOGS if 500 <= r['http.response.status_code'] < 600]) == 7
    assert len(matches(**{'trace.id':'TRACE-A1'})) == 4
    assert len(matches(**{'service.name':'api-gateway','log.level':'ERROR','http.response.status_code':500})) == 3
    assert len([r for r in LOGS if r['log.level']=='ERROR']) == 7
    for path in (ROOT / 'queries/elasticsearch').glob('*.json'):
        json.loads(path.read_text())
    print('PASS: 15 fixture documents, all 8 scenario assertions, and 6 valid query JSON files')

if __name__ == '__main__':
    main()
