# insightcart

# InsightCart

InsightCart is a data analytics platform designed to help mobile market retailers understand their business performance through comprehensive transaction analysis. Built initially for a bakery business operating across multiple London markets, it processes SumUp POS data to provide actionable insights on sales patterns, product performance, and location-based trends.

## Features

### Financial Analytics
- Track daily, weekly and monthly revenue trends
- Analyse payment method distributions
- Monitor transaction values and patterns
- Identify peak trading periods

### Product Analytics
- Track best-selling items by market location
- Analyse product category performance
- Monitor premium product sales
- Evaluate seasonal product trends

### Location Analytics 
- Compare revenue across different market locations
- Visualise customer density patterns
- Identify location-specific product preferences
- Analyse peak trading hours by location

### Time Analytics
- Understand daily trading patterns
- Track weekly performance trends
- Monitor seasonal variations
- Analyse event impact on sales

## Technical Architecture

### Data Pipeline
- Data extraction from SumUp API
- Storage in Supabase PostgreSQL database
- Regular automated updates via Airflow DAGs
- Data anonymisation for public portfolio views

### Database Schema
- Public schema for actual transaction data
- Demo schema with anonymised data
- Comprehensive indexing strategy
- Row-level security implementation

### Tech Stack
- Python for data processing
- Streamlit for dashboard interface
- PostgreSQL (via Supabase) for data storage
- Apache Airflow for orchestration

## Project Structure
```
insightcart/
├── data/                      # Data storage directory
├── dashboard/                 # Streamlit dashboard files
├── pipeline/                  # Data pipeline modules
├── notebooks/                 # Jupyter notebooks for analysis
├── tests/                    # Test files
└── docs/                     # Documentation files
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/insightcart.git
cd insightcart
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your credentials
```

5. Set up the database:
```bash
python setup_database.py
```

## Usage

1. Run the Streamlit dashboard:
```bash
streamlit run Home.py -- --data-path path/to/your/data.json
```

2. Access the dashboard at `http://localhost:8501`

## Configuration

Configuration settings can be modified in `config.py`. Key settings include:
- Database connection parameters
- API authentication details
- Data refresh intervals
- Dashboard customisation options

## Development

### Running Tests
```bash
pytest tests/
```

### Code Style
The project follows PEP 8 guidelines. Format code using:
```bash
black .
```

## Deployment

The application can be deployed in two phases:

### Phase 1: Local Implementation
- Run locally for development and testing
- Single user access
- Manual deployment process

### Phase 2: Cloud Deployment
- Hosted on cloud platform
- Multi-user access with authentication
- Automated deployment pipeline

## Security

- Row-level security enabled on all database tables
- Data anonymisation for public portfolio views
- API key management via environment variables
- Regular security audits and updates

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Contact

Spencer Duvwiama - [LinkedIn](https://www.linkedin.com/feed/)

Project Link: [https://github.com/spencerejd/insightcart](https://github.com/spencerejd/insightcart)

## Acknowledgments

- SumUp API for transaction data access
- Supabase for database hosting
- Streamlit for dashboard framework