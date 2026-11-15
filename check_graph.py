
from workflow.graph import build_workflow

workflow = build_workflow()

print("LangGraph compiled successfully!")

print("\nWorkflow structure:")
print(workflow.get_graph().draw_ascii())
