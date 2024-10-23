# ShopSavvy
Welcome to ShopSavvy! This innovative platform leverages advanced search technologies and natural language processing to enhance the shopping experience, providing users with powerful tools to find and compare products across various eCommerce platforms.

## Project Structure
The ShopSavvy project includes several key components designed for robust data handling, efficient search functionality, and user interaction:

- **Dockerfile**: Defines the environment and commands to containerize the application.
- **deploy.yaml**: Kubernetes deployment configuration for managing services and volumes.
- **es.py**: Integrates Elasticsearch and OpenAI for advanced search and response capabilities.
- **indexMapping.py**: Configuration for Elasticsearch index properties.
- **indexing.py**: Handles the processing and indexing of product data into Elasticsearch.
- **main.py**: The Flask application that serves the web interface and handles all backend operations.

## Features
- **Advanced Product Search**: Utilize Elasticsearch with custom indexing for optimized search results.
- **Machine Learning Integration**: Use OpenAI for generating search query embeddings and responses.
- **Interactive Web Interface**: A Flask-based web interface for easy access and interaction.
- **Containerization and Orchestration**: Use Docker and Kubernetes for deployment and scaling.

## Setup and Installation
### Requirements
- Docker
- Kubernetes (Optional, for deployment using `deploy.yaml`)
- Python 3.x
- Elasticsearch cluster credentials

### Building the Container
1. Clone the repository:
   ```bash
   git clone https://github.com/smaliaquib/ShopSavvy.git
   cd ShopSavvy
   ```

2. Build the Docker container:
   ```bash
   docker build -t shopsavvy-app .
   ```

3. Run the container:
   ```bash
   docker run -p 5000:5000 shopsavvy-app
   ```

### Kubernetes Deployment
To deploy the application using Kubernetes:
1. Apply the YAML configuration:
   ```bash
   kubectl apply -f deploy.yaml
   ```

## Usage
Navigate to `http://localhost:5000` to access the ShopSavvy web interface. Utilize the search functionality to explore product comparisons and details.

## Contributing
Interested in contributing? Great! You can contribute by:
- Submitting bugs and feature requests.
- Reviewing code changes.
- Enhancing the documentation.

Check out [CONTRIBUTING.md](CONTRIBUTING.md) for more information on how to contribute.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact
For major changes, please open an issue first to discuss what you would like to change. For direct communication, you can reach out via [email issue](mailto:email@example.com).

---

### Additional Guidance
- Make sure to adjust the paths and credentials as per your setup.
- For production deployment, ensure environment variables and sensitive credentials are managed securely (e.g., using Kubernetes secrets or environment-specific config files).

