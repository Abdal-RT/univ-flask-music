"""Entrypoint de l’application Flask pour le site d’actualité musicale."""

import importlib.util
import sys
from pathlib import Path

# Import du package `app` depuis le dossier `app/` pour éviter le conflit
# avec le fichier racine `app.py`.
package_dir = Path(__file__).resolve().parent / "app"
spec = importlib.util.spec_from_file_location("app", package_dir / "__init__.py")
app_module = importlib.util.module_from_spec(spec)
sys.modules["app"] = app_module
spec.loader.exec_module(app_module)

app = app_module.create_app()

if __name__ == "__main__":
    app.run(debug=True)
