"""Prüft den Lehrcode mit echten Graphen, ohne Zugangsdaten oder Cloud-Aufrufe."""

from pathlib import Path
import re
import sys

import nbformat
import pytest
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langgraph.errors import GraphRecursionError
from nbclient import NotebookClient
from jupyter_client import KernelManager


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks" / "01_langgraph_quickstart.ipynb"


class ScriptedModel:
    def __init__(self, responses):
        self.responses = iter(responses)
        self.inputs = []

    def invoke(self, messages):
        self.inputs.append(list(messages))
        return next(self.responses)


def call(name, a, b, identifier):
    return {"name": name, "args": {"a": a, "b": b}, "id": identifier, "type": "tool_call"}


@pytest.fixture
def lesson(monkeypatch):
    monkeypatch.chdir(ROOT)
    namespace = {"__name__": "notebook_test"}
    notebook = nbformat.read(NOTEBOOK, as_version=4)
    for index, cell in enumerate(notebook.cells):
        if cell.cell_type == "code" and not {"setup", "live"}.intersection(cell.metadata.get("tags", [])):
            exec(compile(cell.source, f"notebook-cell-{index}", "exec"), namespace)
    return namespace


def run(lesson, responses, question="Addiere 3 und 4.", limit=12):
    model = ScriptedModel(responses)
    lesson["model_with_tools"] = model
    result = lesson["agent"].invoke(
        {"messages": [HumanMessage(content=question)], "llm_calls": 0},
        config={"recursion_limit": limit},
    )
    return result, model


def test_notebook_and_assets():
    notebook = nbformat.read(NOTEBOOK, as_version=4)
    nbformat.validate(notebook)
    for cell in notebook.cells:
        if cell.cell_type == "code":
            compile(cell.source, "notebook", "exec")
            assert cell.outputs == []
            assert cell.execution_count is None
        else:
            for asset in re.findall(r"!\[[^\]]*\]\(([^)]+)\)", cell.source):
                assert (NOTEBOOK.parent / asset).is_file()


def test_tools_and_zero_division(lesson):
    assert lesson["add"].invoke({"a": 3, "b": 4}) == 7
    assert lesson["multiply"].invoke({"a": 7, "b": 5}) == 35
    assert lesson["divide"].invoke({"a": 9, "b": 2}) == 4.5
    assert "Division durch null" in lesson["divide"].invoke({"a": 9, "b": 0})


def test_addition_preserves_context_and_tool_id(lesson):
    result, model = run(lesson, [
        AIMessage(content="", tool_calls=[call("add", 3, 4, "addition-1")]),
        AIMessage(content="3 + 4 = 7."),
    ])
    assert result["llm_calls"] == 2
    assert [m.type for m in result["messages"]] == ["human", "ai", "tool", "ai"]
    tool_result = result["messages"][2]
    assert tool_result.content == "7"
    assert tool_result.tool_call_id == "addition-1"
    assert len(model.inputs[1]) == 4  # System + Human + AI + Tool
    assert model.inputs[1][-1] == tool_result


def test_no_tool_route_and_fresh_state(lesson):
    first, _ = run(lesson, [AIMessage(content="Ich rechne mit Werkzeugen.")])
    second, _ = run(lesson, [AIMessage(content="Neue Antwort.")])
    assert first["llm_calls"] == second["llm_calls"] == 1
    assert len(second["messages"]) == 2
    assert not any(isinstance(m, ToolMessage) for m in first["messages"])


def test_dependent_calculations_in_stream(lesson):
    fake = ScriptedModel([
        AIMessage(content="", tool_calls=[call("add", 3, 4, "step-1")]),
        AIMessage(content="", tool_calls=[call("multiply", 7, 5, "step-2")]),
        AIMessage(content="Das Ergebnis ist 35."),
    ])
    lesson["model_with_tools"] = fake
    updates = list(lesson["agent"].stream(
        {"messages": [HumanMessage(content="(3 + 4) mal 5")], "llm_calls": 0},
        config={"recursion_limit": 12}, stream_mode="updates",
    ))
    assert [next(iter(update)) for update in updates] == [
        "llm_call", "tool_node", "llm_call", "tool_node", "llm_call",
    ]
    assert updates[1]["tool_node"]["messages"][0].content == "7"
    assert updates[3]["tool_node"]["messages"][0].content == "35"
    assert fake.inputs[1][-1].content == "7"
    assert fake.inputs[2][-1].content == "35"
    assert updates[-1]["llm_call"]["llm_calls"] == 3


def test_multiple_tool_calls_and_error_message(lesson):
    result, _ = run(lesson, [
        AIMessage(content="", tool_calls=[call("divide", 4, 0, "zero"), call("add", 2, 3, "sum")]),
        AIMessage(content="Division nicht definiert; Summe 5."),
    ])
    observations = [m for m in result["messages"] if isinstance(m, ToolMessage)]
    assert [m.tool_call_id for m in observations] == ["zero", "sum"]
    assert "Division durch null" in observations[0].content
    assert observations[1].content == "5"


def test_loop_is_bounded(lesson):
    with pytest.raises(GraphRecursionError):
        run(lesson, [AIMessage(content="", tool_calls=[call("add", 1, 1, str(i))]) for i in range(10)], limit=4)


def test_graph_structure(lesson):
    graph = lesson["agent"].get_graph()
    assert set(graph.nodes) == {"__start__", "llm_call", "tool_node", "__end__"}
    assert {(edge.source, edge.target) for edge in graph.edges} == {
        ("__start__", "llm_call"), ("llm_call", "tool_node"),
        ("llm_call", "__end__"), ("tool_node", "llm_call"),
    }


def test_all_cells_in_jupyter_kernel():
    """Auch IPython-Darstellung und beide Beispielzellen prüfen, ohne Cloud-Aufrufe."""
    notebook = nbformat.read(NOTEBOOK, as_version=4)
    for cell in notebook.cells:
        if "setup" in cell.metadata.get("tags", []):
            cell.source = '''from langchain_core.messages import AIMessage
class OfflineModel:
    def __init__(self):
        def call(name, a, b, identifier):
            return AIMessage(content="", tool_calls=[{"name": name, "args": {"a": a, "b": b}, "id": identifier, "type": "tool_call"}])
        self.responses = iter([
            call("add", 3, 4, "a1"), AIMessage(content="3 + 4 = 7."),
            call("add", 3, 4, "b1"), call("multiply", 7, 5, "b2"),
            AIMessage(content="(3 + 4) × 5 = 35."),
        ])
    def invoke(self, messages):
        return next(self.responses)
model_with_tools = OfflineModel()
'''
    manager = KernelManager(kernel_name="python3")
    # Ein vorhandener globaler Kernel darf die Projektumgebung nicht verdrängen.
    manager.kernel_spec.argv[0] = sys.executable
    client = NotebookClient(notebook, km=manager, timeout=60,
                            resources={"metadata": {"path": str(NOTEBOOK.parent)}})
    try:
        executed = client.execute()
    finally:
        if manager.has_kernel:
            manager.shutdown_kernel(now=True)
    for cell in executed.cells:
        if cell.cell_type == "code":
            assert not any(output.output_type == "error" for output in cell.outputs)
    assert executed.cells[23].outputs[-1].text.strip().endswith("Modellaufrufe: 2")
    assert "35" in executed.cells[26].outputs[-1].text
