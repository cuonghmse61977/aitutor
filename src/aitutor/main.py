#!/usr/bin/env python
import csv
import json
import random
import re
import sys
import warnings

from datetime import datetime

from crew import Aitutor

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

print(sys.path)

def run():
    """
    Run the crew.
    """
    inputs = {
        "instruction": "次の計算をしなさい。0  +  (-  5)",
        "question": "{{response}}"
    }
    
    # inputs = {
    #     "instruction": "次の数の絶対値を答えなさい。",
    #     "question": "+10.2+10.2の絶対値  =  {{response}}"
    # }
    try:
        Aitutor().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

def load_data(file_path):
    """Loads JSON data from a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {file_path}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
    
def run_and_save_to_csv(training_file_path, output_csv_path):
    """Runs the AI on the training set and saves the results to a CSV file."""
    training_data = load_data(training_file_path)

    if training_data is None:
        return

    # Take only the first 20 items
    random_items = random.sample(training_data, min(20, len(training_data)))
    training_data = training_data[:20]

    results = []
    for item in training_data:
        instruction = item.get("item_description", "")
        instruction = re.sub(r"{{response}}", "[placeholder]", instruction) #replace {{response}}
        question = item.get("question_content", "")
        question = re.sub(r"{{response}}", "[placeholder]", question) #replace {{response}}
        actual_answer = item.get("options", "") # get the actual answer
        inputs = {
            "instruction": instruction,
            "question": question,
        }
        print(f"Running AI on instruction: {instruction}")
        answer = Aitutor().crew().kickoff(inputs=inputs)
        results.append({"instruction": instruction, "question": question, "actual_answer": actual_answer, "answer": answer})


    # Save results to CSV
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["instruction", "question", "actual_answer", "answer"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow(row)


    print(f"Results saved to {output_csv_path}")

#Edit file here to run
run_and_save_to_csv("src/aitutor/training_set.json", "math_problem_results.csv")

def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        Aitutor().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        Aitutor().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        Aitutor().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
