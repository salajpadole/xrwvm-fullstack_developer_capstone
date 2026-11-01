# fullstack_developer_capstone — DriveWell Dealerships

**IBM Skills Network Fullstack Developer Capstone**

A full-stack dealership discovery and review application built as an IBM Skills Network capstone project.

## Project overview
The application brings dealership discovery, customer reviews, user authentication and car inventory search into one web experience. The project uses a Django backend, a React frontend, and a Node.js/Express microservice backed by MongoDB for car inventory.

## Technology
- React and React Router
- Python and Django
- Node.js and Express
- MongoDB / Mongoose
- SQLite for Django application data
- Docker and Docker Compose
- GitHub Actions (CI/CD workflow, when configured)

## Main capabilities
- Browse dealership locations and filter by state.
- Register and authenticate users.
- View dealership details and customer reviews.
- Submit dealership reviews.
- Search dealer-specific car inventory by make, model, year, mileage and price.
- Analyze review sentiment through the configured sentiment-analysis service.

## Repository structure
```
server/
  djangoapp/          # Django application and API views
  djangoproj/         # Django project configuration
  frontend/           # React application and static pages
  carsInventory/      # Node.js / Express inventory service (if configured)
```

## Local development
Run commands from the appropriate project directories after installing the dependencies and configuring required services.

### Django
```bash
cd server
python3 -m pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:8000
```

### React frontend
```bash
cd server/frontend
npm install
npm run build
```

### Inventory microservice
The inventory service requires a running MongoDB instance and a valid connection configuration. From `server/carsInventory`:
```bash
npm install
node app.js
```

## Configuration and services
Configure database connection strings, service URLs and any credentials through environment variables or local configuration. Do not commit passwords, API keys, tokens or production secrets.

## Demo content
The About Us and Contact Us pages use fictional names and contact details for demonstration. They are not real employees or business contact channels.

## Status
This README describes the intended capstone architecture and features. Verify each service, API endpoint, CI workflow and deployment independently before treating it as operational or production-ready.
