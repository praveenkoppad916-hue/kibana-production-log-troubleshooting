

\# Kibana KQL — Production Log Investigations



\## Project Overview



This project demonstrates six simulated production-support investigations using Kibana Query Language (KQL).



Environment: Elasticsearch + Kibana + Docker



Index: `payment-logs`



Data view: `Payment Logs`



Dataset: 15 synthetic fintech application log events



Investigation date: September 15, 2026



All investigations use fictional data.



\---



\## LOG-001 — Payment Failure Investigation



\### Objective

Trace a failed payment across multiple microservices using a transaction ID.



\### KQL Query

```kql

transaction\_id: "TXN-100245"

```



\### Expected Results

4 matching log events.



\### Findings

\- API gateway accepted the payment.

\- Payment service started processing.

\- Bank adapter returned HTTP 503.

\- Payment service reported transaction failure.



\### Conclusion

The immediate failure trigger was upstream bank-adapter unavailability. The underlying cause requires further investigation.



\---



\## LOG-002 — Upstream Timeout Investigation



\### Objective

Identify transactions affected by upstream service timeouts.



\### KQL Query

```kql

http.response.status\_code: 504

```



\### Expected Results

2 matching log events.



\### Findings

\- Transaction: TXN-100249

\- Bank adapter reported an upstream timeout after 10000 ms.

\- Payment service subsequently reported payment failure.

\- Both events returned HTTP 504.



\### Conclusion

The transaction failed following an upstream timeout. Additional dependency and network evidence is required to determine the underlying cause.



\---



\## LOG-003 — Authentication and Authorization Investigation



\### Objective

Investigate authentication and permission-related failures.



\### KQL Query

```kql

http.response.status\_code: (401 or 403)

```



\### Expected Results

2 matching log events.



\### Findings

\- TXN-100247 returned HTTP 401 due to an invalid authentication token.

\- TXN-100248 returned HTTP 403 due to insufficient permissions.

\- Both events originated from auth-service.



\### Conclusion

The logs show separate authentication and authorization failures.



\---



\## LOG-004 — High Latency and Slow Response Investigation



\### Objective

Identify application events with recorded durations of at least 1000 milliseconds.



\### KQL Query

```kql

event.duration\_ms >= 1000

```



\### Expected Results

4 matching log events.



\### Findings

\- Two events relate to TXN-100245.

\- Two events relate to TXN-100249.

\- Events include HTTP 503 and 504 failures.



\### Conclusion

The filter identifies long-duration events associated with upstream failures. Further analysis is required to distinguish latency causes from downstream failure effects.



\---



\## LOG-005 — Application Error Analysis



\### Objective

Identify ERROR-level application logs across services.



\### KQL Query

```kql

log.level: "ERROR"

```



\### Expected Results

7 matching log events.



\### Findings

\- Bank-adapter unavailability events.

\- Upstream timeout events.

\- Payment-service failure events.

\- API-gateway internal server errors.



\### Conclusion

ERROR-level filtering helps identify incidents requiring deeper investigation and correlation.



\---



\## LOG-006 — HTTP 500 Internal Server Error Investigation



\### Objective

Identify internal server errors originating from application services.



\### KQL Query

```kql

http.response.status\_code: 500

```



\### Expected Results

3 matching log events.



\### Findings

\- Affected transactions: TXN-100251, TXN-100252 and TXN-100253.

\- Service: api-gateway.

\- Message: Unexpected internal error.

\- HTTP response code: 500.



\### Conclusion

Three internal server errors were observed at the API gateway. The underlying technical cause cannot be established from these messages alone.



\---



\## Investigation Workflow



1\. Open Kibana Discover.

2\. Select the Payment Logs data view.

3\. Set the absolute time range to September 15, 2026.

4\. Enter the appropriate KQL query.

5\. Review matching document counts.

6\. Inspect timestamps, transaction IDs, service names, HTTP status codes and log messages.

7\. Correlate related events.

8\. Record technical findings.

9\. Save the investigation in Kibana.

10\. Capture screenshots for evidence.



\## Evidence



Screenshots for all six investigations are stored in the `screenshots/` directory.



\## Skills Demonstrated



\- Kibana Discover

\- Kibana Query Language (KQL)

\- Elasticsearch log investigation

\- Transaction correlation

\- HTTP 4xx and 5xx troubleshooting

\- Application latency analysis

\- Microservices troubleshooting

\- Incident investigation

\- Root cause assessment

\- L2/L3 production support



\## Disclaimer



All logs and transaction identifiers are synthetic. This project is an independent training lab and contains no employer or customer production data.



