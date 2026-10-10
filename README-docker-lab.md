

\# Kibana Production Log Troubleshooting \& Incident RCA Lab



A hands-on L2/L3 production support project demonstrating payment transaction troubleshooting, log correlation, incident investigation, and root cause analysis using Elasticsearch, Kibana, Docker, and KQL.



\## Project Overview



This lab simulates a fintech payment processing environment using 15 synthetic application log events.



The objective is to investigate production-style incidents across multiple services, identify failure patterns, and document evidence-based findings.



All logs are fictional. No employer or customer data is used.



\## Technologies Used



\- Elasticsearch

\- Kibana Discover

\- Kibana Query Language (KQL)

\- Elasticsearch Query DSL

\- Docker and Docker Compose

\- Windows PowerShell

\- JSON and NDJSON



\## Architecture



Synthetic Payment Logs

&#x20;       |

&#x20;       v

Elasticsearch

&#x20;       |

&#x20;       v

Kibana Discover

&#x20;       |

&#x20;       v

KQL Investigations

&#x20;       |

&#x20;       v

Incident Analysis and RCA



\## Investigations



| ID | Investigation | KQL Query | Results |

|---|---|---|---|

| LOG-001 | Payment Failure | `transaction\_id: "TXN-100245"` | 4 |

| LOG-002 | Upstream Timeout | `http.response.status\_code: 504` | 2 |

| LOG-003 | Authentication and Authorization | `http.response.status\_code: (401 or 403)` | 2 |

| LOG-004 | High Latency | `event.duration\_ms >= 1000` | 4 |

| LOG-005 | Error Log Analysis | `log.level: "ERROR"` | 7 |

| LOG-006 | HTTP 500 Internal Server Error | `http.response.status\_code: 500` | 3 |



\## Investigation Evidence



\### LOG-001: Payment Failure



!\[Payment Failure](screenshots/LOG-001-payment-failure.png)



Four correlated events show a payment accepted by the gateway, processing initiated, a bank-adapter failure, and a subsequent payment failure.



\### LOG-002: Upstream Timeout



!\[Upstream Timeout](screenshots/LOG-002-upstream-timeout.png)



Two HTTP 504 events identify an upstream timeout affecting payment processing.



\### LOG-003: Authentication and Authorization



!\[Authentication Investigation](screenshots/LOG-003-authentication.png)



Investigated HTTP 401 and 403 responses to distinguish authentication failures from authorization failures.



\### LOG-004: High Latency



!\[High Latency](screenshots/LOG-004-high-latency.png)



Identified four events with recorded durations of at least 1000 milliseconds.



\### LOG-005: Error Log Analysis



!\[Error Analysis](screenshots/LOG-005-error-analysis.png)



Identified seven ERROR-level events across payment and gateway services.



\### LOG-006: HTTP 500 Errors



!\[HTTP 500 Investigation](screenshots/LOG-006-http-500.png)



Identified three HTTP 500 errors in the API gateway within a 10-second interval.



\## Key Incident Findings



\### Payment Failure ΓÇö TXN-100245



\- Initial gateway request succeeded.

\- Payment processing began.

\- Bank adapter reported HTTP 503.

\- Payment service subsequently reported HTTP 503.

\- Evidence suggests an upstream dependency failure.



\### Upstream Timeout ΓÇö TXN-100249



\- Bank adapter reported an upstream timeout.

\- Payment service recorded the resulting failure.

\- Both events returned HTTP 504.

\- Further dependency monitoring is needed to establish the underlying cause.



\### HTTP 500 Error Cluster



\- Three separate transactions failed.

\- All three errors originated from the API gateway.

\- Events occurred within 10 seconds.

\- A shared application issue is suspected but not confirmed.



\## Skills Demonstrated



\- Production log investigation

\- Transaction ID correlation

\- Multi-service troubleshooting

\- HTTP 4xx and 5xx error analysis

\- Latency investigation

\- Kibana KQL filtering

\- Elasticsearch Query DSL

\- Incident triage

\- Root cause analysis

\- Technical documentation



\## Repository Structure



```text

kibana-docker-lab/

|-- compose.yaml

|-- payment\_logs.ndjson

|-- bulk-import.ndjson

|-- README.md

|-- screenshots/

|-- docs/

|-- queries/

|-- scripts/

```



\## Running the Lab



Start the Docker environment from the project directory:



```powershell

docker compose up -d

```



Open Kibana:



http://localhost:5601



Import the synthetic logs into the `payment-logs` Elasticsearch index using the prepared bulk-import file:



```powershell

curl.exe -X POST "http://localhost:9200/payment-logs/\_bulk?refresh=true" -H "Content-Type: application/x-ndjson" --data-binary "@bulk-import.ndjson"

```



Verify the indexed documents in Kibana Dev Tools:



```http

GET /payment-logs/\_count

```



Expected count: 15.



Create a Kibana data view for `payment-logs`, using `@timestamp` as the time field. Set the Discover time range to September 15ΓÇô16, 2026 to inspect the synthetic events.



\## Disclaimer



This is an independent training project created using synthetic payment application logs. It does not contain real production data, customer information, credentials, or proprietary employer configurations.



