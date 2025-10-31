# NDIS Fraud Detection System

> An AI-powered fraud detection system for National Disability Insurance Scheme (NDIS) invoices using advanced LangChain agents and NIDS pricing validation.

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/docker-ready-brightgreen.svg)](Dockerfile)

## 🎯 Overview

This system provides comprehensive fraud detection for NDIS invoices by:
- ✅ Validating item codes against the official NIDS database
- 💰 Verifying pricing accuracy for standard, remote, and very remote locations
- 📊 Detecting use of outdated pricing from inactive databases
- 🤖 Leveraging AI agents for intelligent analysis
- 🔍 Identifying suspicious patterns and discrepancies

## 🚀 Quick Start

### Prerequisites

- Python 3.13+
- OpenAI API key
- Docker (optional, for containerized deployment)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd agent-demo
   ```

2. **Set up environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY
   ```

4. **Run the application**
   ```bash
   # Streamlit UI
   streamlit run app.py
   
   # Flask API
   python server.py
   
   # CLI Test
   python main.py
   ```

## 📦 Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build

# Access the API
curl http://localhost:5000/health
```

See [Docker Documentation](docs/DOCKER_README.md) for detailed instructions.

## 🏗️ Project Structure

```
agent-demo/
├── agents/              # AI agent implementations
│   ├── ichi.py         # Basic fraud detection agent
│   ├── standard.py     # Comprehensive validation agent
│   ├── models.py       # Data models and schemas
│   └── tools.py        # LangChain tools for NIDS validation
├── data/               # NIDS pricing databases
│   ├── nids_source_active.csv
│   └── nids_source_inactive.csv
├── helpers/            # Utility functions
│   ├── file_helper.py
│   └── steamlist_helper.py
├── tests/              # Test suites
│   ├── test_agent_invoices.py
│   ├── test_pricing_tools.py
│   └── validate_test_data.py
├── docs/               # Documentation
│   ├── README.md
│   └── DOCKER_README.md
├── scripts/            # Utility scripts
│   └── test_docker.sh
├── app.py              # Streamlit web interface
├── server.py           # Flask API server
├── main.py             # CLI interface
└── requirements.txt    # Python dependencies
```

## 🔧 Features

### Agent Types

1. **Standard Agent** - Comprehensive line-by-line validation
   - Validates item codes
   - Checks pricing accuracy
   - Detects old pricing
   - Supports remote/very remote locations

2. **Ichi Agent** - Basic fraud detection
   - Quick fraud pattern detection
   - Invoice-level analysis

### Validation Tools

- **check_nids_item_exists**: Validates item codes against NIDS database
- **check_nids_item_pricing**: Verifies pricing for standard/remote/very remote locations
- **check_if_using_old_pricing**: Detects outdated pricing from inactive database

## 📊 Usage Examples

### CLI Usage

```python
from agents.standard import StandardAgent

agent = StandardAgent(model="gpt-4o")
result = agent.process(invoice_text)

print(f"Valid: {result.is_valid}")
print(f"Reason: {result.reason}")
print(f"Old Pricing: {result.is_using_old_pricing}")
```

### API Usage

```bash
# Health check
curl http://localhost:5000/health

# Root endpoint
curl http://localhost:5000/
```

### Web Interface

```bash
streamlit run app.py
```
Open http://localhost:8501 in your browser.

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Test pricing validation tools
python tests/test_pricing_tools.py

# Test agent with realistic invoices
python tests/test_agent_invoices.py

# Validate test data
python tests/validate_test_data.py
```

**Test Results**: 10/10 tests passed (100% success rate)

See [Test Results](tests/TEST_RESULTS.md) for detailed analysis.

## 📈 Performance

- **Average analysis time**: ~10 seconds per invoice
- **Accuracy**: 100% on test suite
- **Detection types**: Invalid codes, incorrect pricing, outdated pricing, remote pricing mismatches

## 🔐 Security

- API keys stored in environment variables
- Read-only data mounts in Docker
- CORS enabled for API
- Health checks for monitoring

## 🛠️ Development

### Running Tests

```bash
# All tests
python -m pytest tests/

# Specific test
python tests/test_agent_invoices.py

# With coverage
python -m pytest tests/ --cov=agents --cov=helpers
```

### Code Quality

```bash
# Format code
black agents/ helpers/ tests/

# Lint
pylint agents/ helpers/

# Type checking
mypy agents/ helpers/
```

## 📚 Documentation

- [Docker Setup Guide](docs/DOCKER_README.md)
- [Test Results & Analysis](tests/TEST_RESULTS.md)
- [Original README](docs/README.md)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- NIDS pricing data from NDIS official sources
- LangChain for agent framework
- OpenAI for GPT models

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check existing documentation in `/docs`
- Review test examples in `/tests`

---

**Built with ❤️ for NDIS invoice fraud detection**

