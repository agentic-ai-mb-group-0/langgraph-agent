# LangGraph: ein Rechenagent Schritt für Schritt

Ein deutsches **Jupyter-Notebook für den ersten Kontakt mit LangGraph**.

Ein Sprachmodell wählt zwischen drei Rechenwerkzeugen. LangGraph steuert den Ablauf und führt den gemeinsamen Zustand weiter.

→ [Notebook öffnen](notebooks/01_langgraph_quickstart.ipynb)

## Einstieg

Voraussetzungen: Python 3.13 oder 3.14, [uv](https://docs.astral.sh/uv/) und ein [Gemini-API-Key](https://aistudio.google.com/apikey).

```bash
git clone https://github.com/agentic-ai-mb-group-0/langgraph-agent.git
cd langgraph-agent
uv sync --locked
uv run python -m ipykernel install --sys-prefix --name langgraph-agent --display-name "LangGraph · langgraph-agent"
cp .env.example .env
```

In `.env` den eigenen Key eintragen. Alternativ fragt das Notebook den Key verdeckt ab.

```bash
uv run jupyter lab notebooks/01_langgraph_quickstart.ipynb
```

In Jupyter den Kernel **LangGraph · langgraph-agent** wählen. Er ist in der Projektumgebung registriert, nicht global. Nach dem Löschen der `.venv` ist die Registrierung erneut nötig.

Die Zellen von oben nach unten ausführen. Modellaufrufe benötigen Internet und das Kontingent des eigenen Gemini-Zugangs; je nach Tarif entstehen Kosten. Der API-Key bleibt lokal und wird nicht im Notebook gespeichert.

**VS Code:** Notebook öffnen und die Python-Umgebung `.venv` als Kernel auswählen.

## Was im Notebook steckt

| Abschnitt | Kernidee |
|---|---|
| Werkzeuge und Modell | Python rechnet; das Modell wählt das Werkzeug |
| State | Nachrichtenverlauf und Zahl der Modellaufrufe |
| Knoten | Eine Funktion für das Modell, eine für die Werkzeuge |
| Kanten | Weiter zum Werkzeug oder Ende |
| Graph | Den Ablauf zusammensetzen und anzeigen |
| Ausführung | Einen einfachen und einen mehrstufigen Auftrag verfolgen |

Kurze Übungen und aufklappbare Lösungen schließen das Notebook ab.

## Graph anzeigen

Die Darstellung wird **lokal aus dem tatsächlich kompilierten Graphen** erzeugt. Dafür benötigt das Python-Paket `graphviz` zusätzlich das Programm `dot`:

```bash
# macOS
brew install graphviz

# Ubuntu / Debian
sudo apt-get install graphviz

# Windows, mit winget
winget install Graphviz.Graphviz
```

Danach gegebenenfalls Jupyter neu starten. Ohne `dot` zeigt das Notebook den Graphen als Mermaid-Text; der Agent funktioniert trotzdem.

Die zwei zusätzlichen Abbildungen in [assets/](assets/) erklären die Bausteine und den Werkzeugaufruf. Sie wurden mit dem integrierten Bildgenerierungswerkzeug erzeugt. [Prompts und Einordnung](assets/README.md).

## Grundlage und Anpassungen

Grundlage ist das [vollständige Graph-API-Beispiel im offiziellen LangGraph-Quickstart](https://docs.langchain.com/oss/python/langgraph/quickstart#full-code-example).

Der Ablauf bleibt gleich. Die Lehrversion nutzt Gemini passend zu den anderen Demo-Repos, ergänzt deutsche Erklärungen, fängt Division durch null ab und begrenzt die Zahl der Graph-Schritte. Die Graph-Darstellung benötigt keinen externen Mermaid-Dienst.

Zusätzliche Quellen: [Graph API](https://docs.langchain.com/oss/python/langgraph/graph-api), [Gemini-Integration](https://docs.langchain.com/oss/python/integrations/chat/google_generative_ai).

## Prüfung ohne API-Key

```bash
uv run pytest -q
```

Die Tests führen den Notebook-Code mit vorgegebenen Modellantworten durch den echten LangGraph-Graphen aus. Geprüft werden Werkzeuge, Routing, Nachrichtenverlauf, mehrere Rechenschritte und die Schrittgrenze. Es entstehen keine Modellaufrufe.

`uv.lock` hält die geprüften Paketversionen fest. Gespeicherte Notebook-Ausgaben sind bewusst leer, damit keine persönlichen Eingaben oder API-Daten im Repo landen.
