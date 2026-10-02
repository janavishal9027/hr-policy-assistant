"""CLI for the HR Assistant application.

This is the main entry point for the HR Assistant application. It orchestrates the entire process, from loading the HR policy documents, creating embeddings, storing them in a vector store, and setting up the agent to answer user queries.
"""

from hr_assistant.pipeline import ask, build_hr_assistant_agent

def main():
    print("Building the HR policy assistant...")
    agent = build_hr_assistant_agent()  # Build the HR Assistant agent
    print("HR policy assistant is ready to answer your questions. Type 'exit' to quit...")

    demo_questions = [
        "What is the company's policy on remote work?",
        "How many vacation days do I get per year?",
        "What is the procedure for requesting a leave of absence?"
    ]

    for question in demo_questions:
        print("=" * 60)
        print(f"Question: {question}")
        print("-" * 60)
        answer = ask(agent, question)  # Ask the question to the agent
        print(f"Answer: {answer}")
        print("=" * 60)
        print()


if __name__ == "__main__":
    main()  # Run the main function to start the HR Assistant application