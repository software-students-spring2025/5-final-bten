"""mlclient.py"""

# pylint: disable=unused-import

import os
from contextlib import redirect_stdout
from typing import Dict, Any
import sys
import io
import json
import traceback
import requests

# pylint: disable=E0401

from llama_index.core.tools import FunctionTool
from llama_index.core.agent import ReActAgent
from llama_index.llms.openai import OpenAI

def set_api_key(key):
    """This sets the environment API key"""
    os.environ["OPENAI_API_KEY"] = str(key)


BASE_MEALDB_API_URL = "https://www.themealdb.com/api/json/v1/1/"


def call_mealdb_api(endpoint: str, params: Dict[str, str]) -> dict:
    """function to access the public MealDB API endpoints which has the recipies"""
    url = f"{BASE_MEALDB_API_URL}{endpoint}"

    print(f"\nAttempting API Call: {url} with params {params}")
    try:
        response = requests.get(url, params=params, timeout=60)
        response.raise_for_status()
        data = response.json()
        # this is the response
        print("API Success")
        return data
    except requests.exceptions.RequestException as e:
        # This print will be captured
        print(f"API Error: {e}")
        return {"error": f"{e}", "meals": "None"}


def filter_by_ingredient(ingredient: str) -> dict:
    """This finds a list of meals form the db containing a specific primary
    ingredient. It returns a dict containing a list of meals with title and info,
    specifically idMeal allows further searching of recipe details"""

    # no spaces
    formatted_ingredient = ingredient.replace(" ", "_").lower()
    return call_mealdb_api("filter.php", {"i": formatted_ingredient})


def lookup_recipe_by_id(meal_id: str) -> dict:
    """Looks up the FULL details for a singl emeal with its specific id
    trurns a dictionary with a meals key containing a list of one meal's
    recipe instructions 'strInstructions' or {'meals': None} if the id is not found"""

    if not meal_id or not meal_id.isdigit():
        print(
            f"Debug lookup_recipie_by_id tool Error: Invalid meal_id provided: {meal_id}"
        )
        return {
            "error": f"Debug lookup_recipie_by_id tool Error: Invalid meal_id provided: {meal_id}"
        }
    return call_mealdb_api("lookup.php", {"i": meal_id})


# LlamaIndex part
def initialize_agent():
    """ initialize the LlamaIndex ReAct agent """

    ingredient_tool = FunctionTool.from_defaults(
        fn=filter_by_ingredient,
        name="filter_by_ingredient",
        description="""Use this tool FIRST to get a list of meal names and IDs based on a single primary ingredient
    This provides options but not full recipes""",
    )

    recipe_lookup_tool = FunctionTool.from_defaults(
        fn=lookup_recipe_by_id,
        name="lookup_recipe_by_id",
        description="""Use this tool SECOND, provide a specific numeric meal ID (obtained from 'filter_by_ingredient' tool)
    to get the full recipe details, including ingredients and instructions""",
    )


    # LLM Setup
    try:
        llm = OpenAI(model="gpt-4.1-mini")  # This model seems to work
    except Exception as e:
        print(f"CRITICAL: Error initializing LLM. check OPENAI_API_KEY set? {e}")
        sys.exit(1)

    # ReAct Agent setup
    agent = ReActAgent.from_tools(
        tools=[ingredient_tool, recipe_lookup_tool], llm=llm, verbose=True
    )

    return agent

# getting the agent output


def print_agent_output(output_data: Dict[str, Any]):
    """Prints the captured logs and final response from the agentic LlamaIndex ReAct agent as dict"""
    print("- Agent Logs with Tool inputs")
    log_output = output_data.get("verbose_log_and_tool_prints")
    print(log_output if log_output else "No stdout captured.")

    print("\n")
    print("- Final Agent Response -")
    print("\n")
    final_response = output_data.get("final_agent_response")
    print(final_response if final_response else "No final response captured.")


def get_recipe_reccomendation(user_input) -> Dict[str, Any]:
    """Process user input and return recipe recommendations using the LlamaIndex agent, runs the thing"""
    agent = initialize_agent()
    stdout_capture_buffer = io.StringIO()
    captured_stdout_log = None
    agent_response = None

    with redirect_stdout(stdout_capture_buffer):
        try:
            agent_query = (
                f"User query: '{user_input}'."
                """#YOUR GOAL: Based on the user's ingredients and preferences,
                FIRST find relevant meal IDs using 'filter_by_ingredient'.
                THEN select the best matching meal ID based on
                user preferences (if any). NEXT, use 'lookup_recipe_by-id' with the selected ID to get the full recipe.
                FINALLY extract and return the cooking instructions (from 'strInstructions'), and some comments wishing the user well
                for their goals. If no specific preference beyond ingredient is given, you can choose one, make a comment about how/why you think the
                user might like it.
                """
            )
            # Execute the agent
            agent_response = agent.chat(agent_query)

        except Exception as e:
            print("\n Error during agent execution")
            print(f"The error is : {e}")
            agent_response = f"Agent execution failed: {str(e)}"

    captured_stdout_log = stdout_capture_buffer.getvalue()

    agent_output_dict = {
        "recipe": str(agent_response),
        "reasons": captured_stdout_log,
        "inputs": user_input
    }

    agent_output_string = " "

    agent_output_string += "----------Recipe----------\n"
    agent_output_string += agent_output_dict["recipe"]
    agent_output_string += "\n" + "\n"
    agent_output_string += "-----------Why We Chose This Recipe For You----------\n"
    agent_output_string += "-----------(our AI's agent's thoughts and internet accesses)----------\n"
    agent_output_string += agent_output_dict["reasons"]
    agent_output_string += "\n" + "\n"
    agent_output_string += "-----------Given these inputs----------\n"
    agent_output_string += agent_output_dict["inputs"]


    return agent_output_string



# test, will need to find out how to integrate this into the app

if __name__ == "__main__":
    user_input = input(
        "Enter some ingredients, a main ingredient, and a style of dish such as 'continental'"
    )

    result = get_recipe_reccomendation(user_input)
    print(result.get("verbose_log_and_tool_prints", "No stdout"))
    print(result.get("final_agent_response", "No final response captured."))


# pylint: disable=W0105

'''
reference from old main:
stdout_capture_buffer = io.StringIO()
captured_stdout_log = None
agent_response = None

with redirect_stdout(stdout_capture_buffer):
    try:
        agent_query = (
            f"User query: '{user_input}'."
            """#YOUR GOAL: Based on the user's ingredients and preferences,
             FIRST find
        relevant meal IDs using 'filter_by_ingredient'.
        THEN select the best matching meal ID based on
        user preferences (if any). NEXT, use 'lookup_recipe_by-id' with the selected ID to get the full recipe.
        FINALLY extraact and return the cooking instructions( from 'strInstructions'), and some comments wishing the user well
        for their goals. If no specific preference beyond ingredient is given, you can choose one, make a comment about how/why you think the
        user might like it.
        """
        )
        # note this part makes it go
        agent_response = agent.chat(agent_query)

    except Exception as e:
        print("\n Error during agent execution")
        print(f"The error is : {e}")
        agent_response = "Agent execution failed see cap. logs."

captured_stdout_log = stdout_capture_buffer.getvalue()

agent_output_dict_test = {
    "verbose_log_and_tool_prints": captured_stdout_log,
    "final_agent_response": agent_response,
}

# This part is just debug
print_agent_output(agent_output_dict_test)

'''
