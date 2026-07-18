# ReviewPilot 🚀

> **Enterprise AI Pull Request Review Platform**

ReviewPilot is a production-ready, AI-powered developer tool that acts as a Staff Engineer for your pull requests. It combines robust traditional static analysis with the analytical reasoning capabilities of LLMs to review code for performance, security, architecture, and maintainability.

---

## 🌟 Features

- **Automated AI Reviews**: Deep, contextual code analysis powered by Groq and LLaMA 3.
- **Static Analysis Integration**: Runs Ruff, ESLint, cppcheck, and more directly on your codebase to supply the AI with deterministic findings.
- **Enterprise Dashboard**: Beautiful, responsive, dark-mode first UI built with Next.js 15, Tailwind CSS, and shadcn/ui.
- **Developer Metrics**: Track review history, average scores, and merge-readiness across your team over time.
- **Secure & Scalable**: JWT Authentication, PostgreSQL database, and Redis caching wrapped in a strict Clean Architecture pattern.

## 🏗️ Architecture

ReviewPilot is composed of a Next.js 15 frontend and a FastAPI backend. It utilizes a factory pattern for static analysis and abstract provider interfaces for LLMs, allowing seamless integration with OpenAI, Anthropic, or Gemini.

- **Frontend**: Next.js 15 (App Router), React, Tailwind CSS, shadcn/ui, Recharts, Framer Motion.
- **Backend**: Python, FastAPI, SQLAlchemy, Alembic, PostgreSQL, Redis.
- **Deployment**: Docker, Docker Compose, Multi-stage builds.

## 🚀 Getting Started

### Prerequisites

- Docker and Docker Compose installed.
- A Groq API Key (or OpenAI/Anthropic depending on the configured provider).

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/ReviewPilot.git
   cd ReviewPilot
   ```

2. **Set your environment variables:**
   Create a `.env` file in the root directory (or simply export the variable):
   ```bash
   export GROQ_API_KEY="your-api-key-here"
   ```

3. **Build and start the platform:**
   ```bash
   make build
   make up
   ```

4. **Run Database Migrations:**
   ```bash
   make migrate
   ```

5. **Access the Application:**
   - **Frontend:** http://localhost:3000
   - **Backend API Docs:** http://localhost:8000/docs

## 🛠️ Makefile Commands

- `make build` - Build all Docker images.
- `make up` - Start all services in the background.
- `make down` - Stop all services and remove containers.
- `make logs` - View logs from all services.
- `make db-shell` - Access the PostgreSQL shell.
- `make migrate` - Run database migrations (Alembic).
- `make status` - View the status of all running containers.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

## 📄 License

This project is licensed under the MIT License.
