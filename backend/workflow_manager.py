# backend/workflow_manager.py

import yaml


def execute_workflow(user, workflow_name):
    """
    Execute a workflow for a specific user.
    This function loads the workflow from YAML and executes each step.
    """
    # Load the workflow definition from YAML
    workflow_path = f"workflows/{workflow_name}.yaml"
    with open(workflow_path, "r") as file:
        workflow = yaml.safe_load(file)
    
    print(f"User {user} is executing the workflow: {workflow_name}")
    
    # Execute each step in the workflow
    for step in workflow['steps']:
        action = step['action']
        if action == "open_application":
            print(f"Opening application: {step['application']}")
        elif action == "check_email":
            print("Checking email")
        # Add more workflow step handling logic
