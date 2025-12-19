"""
Project templates for common application types.
"""
from typing import Dict, List
from pydantic import BaseModel


class ProjectTemplate(BaseModel):
    name: str
    description: str
    techstack: str
    features: List[str]
    files: Dict[str, str]  # filename: purpose
    required_packages: List[str]
    enable_docker: bool = False
    enable_ci_cd: bool = False


# Template definitions
TEMPLATES = {
    "fastapi-rest-api": ProjectTemplate(
        name="FastAPI REST API",
        description="A modern REST API built with FastAPI, including authentication, database, and documentation",
        techstack="python, fastapi, sqlalchemy, postgresql",
        features=[
            "RESTful API endpoints",
            "JWT authentication",
            "Database models with SQLAlchemy",
            "Automatic API documentation",
            "CORS middleware",
            "Environment configuration",
            "Logging and error handling"
        ],
        files={
            "main.py": "FastAPI application entry point",
            "models.py": "SQLAlchemy database models",
            "schemas.py": "Pydantic request/response schemas",
            "crud.py": "Database CRUD operations",
            "auth.py": "Authentication and authorization",
            "database.py": "Database connection and session",
            "config.py": "Configuration management",
            "routers/users.py": "User management endpoints",
            "routers/items.py": "Item management endpoints",
            "requirements.txt": "Python dependencies"
        },
        required_packages=[
            "fastapi",
            "uvicorn[standard]",
            "sqlalchemy",
            "psycopg2-binary",
            "python-jose[cryptography]",
            "passlib[bcrypt]",
            "python-multipart",
            "pydantic-settings"
        ],
        enable_docker=True,
        enable_ci_cd=True
    ),
    
    "react-spa": ProjectTemplate(
        name="React SPA",
        description="A modern single-page application with React, TypeScript, and Material-UI",
        techstack="react, typescript, material-ui, react-router",
        features=[
            "TypeScript for type safety",
            "Material-UI components",
            "React Router for navigation",
            "State management with Context API",
            "Responsive design",
            "API integration with axios",
            "Form validation",
            "Dark mode support"
        ],
        files={
            "src/App.tsx": "Main application component",
            "src/index.tsx": "Application entry point",
            "src/components/Header.tsx": "Header component",
            "src/components/Sidebar.tsx": "Sidebar navigation",
            "src/pages/Home.tsx": "Home page",
            "src/pages/About.tsx": "About page",
            "src/contexts/ThemeContext.tsx": "Theme context provider",
            "src/services/api.ts": "API service layer",
            "src/types/index.ts": "TypeScript type definitions",
            "package.json": "Node.js dependencies",
            "tsconfig.json": "TypeScript configuration"
        },
        required_packages=[
            "react",
            "react-dom",
            "react-router-dom",
            "@mui/material",
            "@emotion/react",
            "@emotion/styled",
            "axios",
            "typescript",
            "@types/react",
            "@types/react-dom"
        ],
        enable_docker=True,
        enable_ci_cd=True
    ),
    
    "django-webapp": ProjectTemplate(
        name="Django Web Application",
        description="Full-featured Django web application with admin panel, authentication, and database",
        techstack="python, django, postgresql, bootstrap",
        features=[
            "Django admin interface",
            "User authentication system",
            "Database models and migrations",
            "Template-based views",
            "Form handling and validation",
            "Static files management",
            "URL routing",
            "Middleware configuration"
        ],
        files={
            "manage.py": "Django management script",
            "myapp/settings.py": "Django settings",
            "myapp/urls.py": "URL configuration",
            "myapp/wsgi.py": "WSGI configuration",
            "app/models.py": "Database models",
            "app/views.py": "View functions",
            "app/forms.py": "Form definitions",
            "app/admin.py": "Admin configuration",
            "app/urls.py": "App URL patterns",
            "templates/base.html": "Base template",
            "requirements.txt": "Python dependencies"
        },
        required_packages=[
            "Django>=4.2",
            "psycopg2-binary",
            "python-decouple",
            "whitenoise",
            "pillow"
        ],
        enable_docker=True,
        enable_ci_cd=True
    ),
    
    "flask-microservice": ProjectTemplate(
        name="Flask Microservice",
        description="Lightweight Flask microservice with REST API, database, and Docker support",
        techstack="python, flask, sqlalchemy, redis",
        features=[
            "RESTful API endpoints",
            "Database integration",
            "Redis caching",
            "Request validation",
            "Error handling",
            "Logging configuration",
            "Health check endpoint",
            "Docker containerization"
        ],
        files={
            "app.py": "Flask application",
            "models.py": "Database models",
            "routes.py": "API routes",
            "config.py": "Configuration",
            "extensions.py": "Flask extensions",
            "utils.py": "Utility functions",
            "requirements.txt": "Dependencies"
        },
        required_packages=[
            "Flask",
            "Flask-SQLAlchemy",
            "Flask-CORS",
            "redis",
            "python-dotenv",
            "gunicorn"
        ],
        enable_docker=True,
        enable_ci_cd=False
    ),
    
    "nextjs-fullstack": ProjectTemplate(
        name="Next.js Full-Stack App",
        description="Modern full-stack application with Next.js, TypeScript, and API routes",
        techstack="nextjs, typescript, tailwindcss, prisma",
        features=[
            "Server-side rendering",
            "API routes",
            "TypeScript throughout",
            "Tailwind CSS styling",
            "Prisma ORM",
            "Authentication",
            "SEO optimization",
            "Image optimization"
        ],
        files={
            "pages/index.tsx": "Home page",
            "pages/_app.tsx": "App component",
            "pages/api/users.ts": "User API route",
            "components/Layout.tsx": "Layout component",
            "lib/prisma.ts": "Prisma client",
            "styles/globals.css": "Global styles",
            "package.json": "Dependencies",
            "tsconfig.json": "TypeScript config",
            "tailwind.config.js": "Tailwind config"
        },
        required_packages=[
            "next",
            "react",
            "react-dom",
            "typescript",
            "@types/react",
            "tailwindcss",
            "postcss",
            "autoprefixer",
            "@prisma/client",
            "prisma"
        ],
        enable_docker=True,
        enable_ci_cd=True
    ),
    
    "python-cli-tool": ProjectTemplate(
        name="Python CLI Tool",
        description="Command-line interface tool with Click, configuration, and packaging",
        techstack="python, click, rich",
        features=[
            "Command-line interface",
            "Subcommands support",
            "Configuration file handling",
            "Rich terminal output",
            "Progress bars",
            "Error handling",
            "Logging",
            "Package distribution"
        ],
        files={
            "cli.py": "Main CLI entry point",
            "commands/init.py": "Init command",
            "commands/run.py": "Run command",
            "utils/config.py": "Configuration management",
            "utils/logger.py": "Logging setup",
            "setup.py": "Package setup",
            "requirements.txt": "Dependencies"
        },
        required_packages=[
            "click",
            "rich",
            "pyyaml",
            "python-dotenv"
        ],
        enable_docker=False,
        enable_ci_cd=True
    ),
    
    "data-pipeline": ProjectTemplate(
        name="Data Pipeline",
        description="ETL data pipeline with Apache Airflow, Pandas, and data validation",
        techstack="python, airflow, pandas, sql",
        features=[
            "Apache Airflow DAGs",
            "Data extraction",
            "Data transformation",
            "Data loading",
            "Data validation",
            "Error handling",
            "Monitoring",
            "Scheduling"
        ],
        files={
            "dags/etl_pipeline.py": "Main ETL DAG",
            "scripts/extract.py": "Data extraction",
            "scripts/transform.py": "Data transformation",
            "scripts/load.py": "Data loading",
            "utils/validators.py": "Data validators",
            "config/pipeline_config.yaml": "Pipeline configuration",
            "requirements.txt": "Dependencies"
        },
        required_packages=[
            "apache-airflow",
            "pandas",
            "sqlalchemy",
            "great-expectations",
            "pyyaml"
        ],
        enable_docker=True,
        enable_ci_cd=False
    )
}


def get_template(template_name: str) -> ProjectTemplate:
    """Get a project template by name."""
    return TEMPLATES.get(template_name)


def list_templates() -> List[str]:
    """List all available template names."""
    return list(TEMPLATES.keys())


def get_template_info(template_name: str) -> dict:
    """Get template information."""
    template = get_template(template_name)
    if template:
        return {
            "name": template.name,
            "description": template.description,
            "techstack": template.techstack,
            "features": template.features,
            "file_count": len(template.files)
        }
    return None
