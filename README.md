# Kelson

> **Batteries-included Machine Learning Framework.**  
> Move your ML code out of messy notebooks and into a structured, elegant codebase.

Kelson is an opinionated Python framework that brings the structure and developer experience of modern web frameworks (like Laravel or Django) to Machine Learning engineering. It provides a standard directory structure, a powerful CLI, dependency injection, and beautiful output.

## 🚀 Features

- **Standard Directory Structure**: Stop guessing where to put your data, models, or config.
- **CLI Engine**: Powerful `kelson` command for scaffolding and management.
- **Abstract Base Models**: Enforced interface (`load_data`, `transform`, `build`, `fit`) using Pydantic.
- **Configuration Management**: Centralized `config/ml.yaml` for hyperparameters—no more hardcoding.
- **Training Dashboard**: Beautiful, real-time terminal dashboard with progress bars and metrics tables using [Rich](https://github.com/Textualize/rich).
- **Service Container**: Simple dependency injection to swap components (like DataLoaders) via config.

## 📦 Installation

```bash
pip install kelson
```

*(Note: While in development, clone the repo and run `pip install -e .`)*

## ⚡ Quick Start

### 1. Create a New Project

```bash
kelson new my-ml-app
cd my-ml-app
pip install -e .
```

This generates a structured project:

```
my-ml-app/
├── app/
│   ├── Models/       # Your model architectures
│   └── Pipelines/    # Data processing logic
├── config/
│   ├── ml.yaml       # Hyperparameters & paths
│   └── app.yaml      # App configuration
├── database/
│   └── datasets/     # Raw and processed data
├── storage/          # Checkpoints and logs
└── pyproject.toml
```

### 2. Scaffold a Model

Generate a new model class with boilerplate code:

```bash
kelson make:model IrisClassifier
```

This creates `app/Models/iris_classifier.py`.

### 3. Define Your Model

Edit `app/Models/iris_classifier.py`. Kelson enforces a standard structure:

```python
from kelson.core.model import BaseModel
from typing import Any

class IrisClassifier(BaseModel):
    # Hyperparameters (automatically injected from config/ml.yaml)
    learning_rate: float = 0.001
    batch_size: int = 32

    def fit(self, data: Any) -> Any:
        for epoch in range(10):
            # ... training logic ...
            
            # Log metrics to the beautiful CLI dashboard
            self.log({
                "epoch": epoch + 1, 
                "loss": 0.5, 
                "accuracy": 0.95
            })
```

### 4. Configure Hyperparameters

Open `config/ml.yaml`:

```yaml
models:
  IrisClassifier:
    learning_rate: 0.01
    batch_size: 64
```

### 5. Train

Run the training loop with the built-in dashboard:

```bash
kelson train IrisClassifier
```

## 🛠 Command Reference

| Command | Description |
|---------|-------------|
| `kelson new <name>` | Create a new Kelson project |
| `kelson make:model <Name>` | Scaffold a new model class |
| `kelson train <Name>` | Train a model with the dashboard |

## 🧩 Philosophy

Data Science often suffers from "Notebook Fatigue"—code hidden in cells, global variables everywhere, and no reproducibility. Kelson solves this by treating ML models as **software engineering artifacts**.

- **Convention over Configuration**: Defaults work out of the box.
- **Type Safety**: Built on Pydantic and Type Hints.
- **Developer Experience**: CLI tools and beautiful output make ML fun again.

## 📄 License

MIT License.
