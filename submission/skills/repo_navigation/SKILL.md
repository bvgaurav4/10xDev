<!-- ---
name: repo_navigation
description: Navigate code repositories, locate implementations, and trace dependencies using repository search and code-graph tools.
--- -->

# Repository Navigation

## Purpose

Help the agent understand an unfamiliar codebase, locate relevant implementations, and trace how components interact.

## When to Use

Use this skill when:
- Finding where a function, class, or feature is implemented.
- Understanding how a request flows through the application.
- Identifying callers, dependencies, and related modules.
- Investigating bugs that span multiple files.
- Understanding the impact of a proposed code change.

## Workflow

1. **Understand the task**
   - Identify the feature, symbol, error, or behavior being investigated.
   - Extract relevant names, keywords, and expected behavior.

2. **Search the repository**
   - Use `search_similar_code` to locate semantically relevant code.
   - Search for exact function names, classes, and error messages when available.
   - Avoid assuming that the first search result is the correct implementation.

3. **Trace dependencies**
   - Use `get_code_neighbors` to inspect connected symbols and dependencies.
   - Use `get_code_subgraph` to understand larger relationships between components.
   - Identify callers, callees, interfaces, and important data flows.
   - Use `search_repo` to get the nodes involded in the problem statement.
   - Use `custom_script_execution` for any additional scripts required .

4. **Read the source**
   - Use `read_file` to inspect relevant source files.
   - Verify important conclusions against actual code rather than relying only on graph metadata.

5. **Construct the explanation**
   - Explain the relevant execution path.
   - Identify the files and symbols involved.
   - Distinguish verified facts from assumptions.
   - If evidence is insufficient, continue investigating instead of inventing details.

6. **Additional Code analysis**
  - This includes analyze change impact , find related tests, and trace execution flow
  - Generate the python script needed perform the respective task and use `custom_script_execution` to execute this 

## Guidelines

- Prefer focused searches over exploring the entire repository.
- Follow the actual control flow and data flow.
- Inspect tests and configuration files when they affect the behavior.
- Do not modify source files unless explicitly requested.
- Keep the final explanation concise and reference relevant file paths and symbols.

## Available Resources

Consult any scripts and reference documents included in this skill directory when they are relevant to the investigation.