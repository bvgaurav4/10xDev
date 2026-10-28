## Code Analysis

- For each Functional Requirement (FR), identify the relevant code nodes using `scripts.get_repo_nodes` and `scripts.search_repo`. If the existing scripts are insufficient, use `scripts.custom_script_execution` to perform additional repository analysis dynamically.
- Follow the instructions and workflows defined in `submission/skills/repo_navigation/SKILL.md` when navigating the repository, tracing dependencies, and analyzing code.
- Map out all the Edge cases and highlight them.
- Inspect the relevant source files to verify the identified nodes, understand the execution flow, and determine how the existing implementation relates to each FR.
- Identify the files and components that require changes, their dependencies, potential side effects, and relevant tests.
- Create a Markdown file in the designated workspace containing the complete analysis and proposed code change plan. Organize it by FR and include:
  - Relevant files, symbols, and code locations.
  - Existing implementation and execution flow.
  - Required changes and their rationale.
  - Dependencies, edge cases, and potential regression risks.
  - Relevant tests and a validation strategy.
- Base conclusions on inspected code and available evidence. Clearly distinguish verified findings from assumptions, and do not modify source code during the analysis phase.


## Code Modification 
- Use `edit_file` for changes to existing code. Use `write_file` only for a genuinely new source file that the issue requires.
- Copy the `edit_file` old_string exactly from the code you read and make it unique. If an edit fails to match, reread that region and retry with a shorter unique snippet; never repeat an identical failed call.
- Fix the cause, not the symptom. Do not special-case the example from the issue.
- Change only what the issue requires. Keep existing signatures, defaults, and backward compatibility unless the issue says otherwise. Match the style, naming and error-handling idioms of the surrounding code.
- Use the exact exception class and exact message text from the issue. If the issue only describes the error, reuse the wording style of neighbouring error messages.
- Handle every edge case you listed in step 1.
- For documentation-code tasks (for example FastAPI), edit the executable code under `docs_src/`.