# Natural Language to SQL Demo

Convert a few constrained requests into example SQL without executing queries.

## What this project demonstrates

- A small, runnable Python application.
- Clear input and JSON output.
- Automated tests using Python's built-in `unittest`.
- Basic error handling and documented limitations.

## Requirements

- Python 3.10 or newer
- Git (for development)

No third-party Python packages or paid API keys are required.

## Quick start

```powershell
python --version
python app.py --input "Show me a demo"
```

## Examples

```powershell
python app.py --input "How many records are there?"
python -m unittest discover -s tests -v
```

Some projects accept more specific input:

- **Data analyst:** `python app.py --data sample.csv`
- **Invoice processor:** provide newline-separated fields, such as `Invoice_Number: INV-101`, `Vendor: Example Ltd`, `Date: 2026-01-10`, `Total: 1250`
- **Resume matcher:** separate resume text and job description with a line containing `---JOB---`.
- **Fact checker:** put the claim on the first line and any supplied evidence on later lines.

## Project scope

This is a portfolio demonstration intended for learning and extension. It does not claim to be a production service. Some projects use local rules or simulated steps instead of a real LLM, external research, or database.

## Suggested improvements

1. Add a web interface or API.
2. Add structured logging and input validation.
3. Add integration tests and continuous integration.
4. For an AI version, integrate a model only after configuring its API key securely through environment variables or a secrets manager.
5. Review privacy, security, and accuracy before using real customer data.

## Security

Do not commit passwords, API keys, access tokens, private customer data, or `.env` files.

## License

MIT. See `LICENSE`.
