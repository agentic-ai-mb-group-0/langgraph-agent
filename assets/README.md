# Abbildungen

Die Abbildungen sind didaktische Illustrationen, erzeugt am 30. September 2026 mit dem integrierten Codex-Bildgenerierungswerkzeug (`image_gen`, Skill `imagegen`). Sie wurden visuell auf Text und fachliche Aussage geprüft.

- `agenten-bausteine.png`: Rollen von State, Modell und Werkzeugen. Die Anordnung zeigt keinen zeitlichen Ablauf.
- `tool-aufruf.png`: Ein möglicher Durchlauf für die Addition von 3 und 4. Werkzeugauswahl und Antwortformulierung können bei einem echten Modell abweichen.

Die exakte Graphstruktur zeigt separat die aus dem kompilierten Graphen erzeugte Darstellung im Notebook.

## Prompt: Bausteine

Create a polished German educational illustration for a Jupyter notebook introducing LangGraph to university students. Landscape 3:2, white background, generous whitespace, calm Apple editorial aesthetic, navy text, restrained blue teal lavender accents, beautifully crafted soft dimensional paper objects, no robot mascots, no logos. Title exact: 'Drei Bausteine eines Agenten'. Three equally sized distinct areas in a row: left a stack of message cards titled 'State', subtitle 'Speichert Nachrichten'; middle an abstract language model represented by softly glowing geometric object titled 'Modell', subtitle 'Wählt den nächsten Schritt'; right a calculator and three small blocks + × ÷ titled 'Tools', subtitle 'Führen Python-Code aus'. No directional arrows, because this is an overview of roles rather than execution order. Large very readable German typography, all text exact and correct, not too much text. Save as an educational image.

## Prompt: Werkzeugaufruf

Create a polished German educational infographic illustration for a Jupyter notebook about LangGraph tool calling. Landscape 3:2, white background, ample whitespace, calm Apple editorial aesthetic, navy text and restrained blue teal lavender accents, beautifully crafted soft dimensional cards. Title exact 'Vom Auftrag zur Antwort'. Show a single left-to-right sequence with 5 large rounded cards and arrows between each adjacent pair, with enough spacing: 1 card heading 'Auftrag', content '3 + 4'; 2 heading 'Modell', content 'add(a=3, b=4)'; 3 heading 'Python-Tool', content 'Ergebnis: 7'; 4 heading 'Modell', content 'Nutzt das Ergebnis'; 5 heading 'Antwort', content '3 + 4 = 7'. Model icons abstract geometric, tool calculator icon. Under sequence a discreet continuous strip with label exact 'State: Der Nachrichtenverlauf wächst mit jedem Schritt'. Make all wording correct and large legible. This is an exemplary execution trace, not a claim that every prompt needs a tool. No extra text, no robot, no code apart from add(a=3, b=4).
