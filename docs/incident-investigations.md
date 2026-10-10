# Six reproducible investigations

All findings below are **derived from the 15 synthetic documents** in `data/payment_logs.ndjson`. These are training scenarios, not real production incidents.

| Lab | Search in Kibana Discover (KQL mode) | Expected hits | Interpretation |
|---|---|---:|---|
| LOG-001 | `transaction_id: "TXN-100245"` | 4 | Gateway received request; payment service started; bank adapter returned 503; payment service failed. |
| LOG-002 | `http.response.status_code: 504` | 2 | Bank adapter timeout and propagated payment failure for TXN-100249. |
| LOG-003 | `http.response.status_code: (401 or 403)` | 2 | One invalid token (401), one permission denial (403). |
| LOG-004 | `http.response.status_code >= 500 and http.response.status_code < 600` | 7 | All server-side failures in fixture. |
| LOG-005 | `trace.id: "TRACE-A1"` | 4 | Correlates three services using shared trace ID. |
| LOG-006 | `service.name: "api-gateway" and log.level: "ERROR" and http.response.status_code: 500` | 3 | Three errors at 10:06:00, 10:06:05, 10:06:10 UTC. |

## Example incident report: LOG-001

**Impact:** Synthetic payment TXN-100245 failed. No real customer affected.

**Timeline (UTC):** 10:00:00 gateway received payment; 10:00:01 payment service began processing; 10:00:02 bank adapter reported 503; 10:00:03 payment service recorded failure.

**Observed cause:** The bank adapter was unavailable (HTTP 503). The fixture supports this immediate cause; it does **not** establish why the upstream service was unavailable.

**Suggested follow-up:** Check upstream health and incident status; review retries and circuit breaker settings; confirm customer-facing status. These are recommendations, not facts established by the fixture.

**Evidence:** Filter `transaction_id: "TXN-100245"`, sort `@timestamp` ascending, inspect `trace.id: "TRACE-A1"`.

## Verification caveats

- KQL is a **filter language in Kibana Discover**, not an Elasticsearch `_search` JSON body.
- The JSON files under `queries/elasticsearch/` use Elasticsearch Query DSL.
- The offline tests verify fixture counts and JSON syntax. **They do not execute KQL or Query DSL in a running Elastic cluster.** Follow the optional live setup to validate engine behavior.
- Field names use literal dotted keys and require an appropriate mapping. Avoid default text-only dynamic mappings for exact `term` queries.
- Use UTC date/time range covering `2026-09-15T10:00:00Z` to `2026-09-15T10:07:00Z`; otherwise Kibana can show zero results.
