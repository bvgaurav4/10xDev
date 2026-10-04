### `search_repo`

Search and analyze the repository using its precomputed code graph and embeddings. Use this tool to explore relationships between code symbols, find structural neighbors such as callers and callees, identify semantically similar code, and inspect the local subgraph around a relevant symbol. Useful for understanding how a piece of code connects to the rest of the repository and for tracing potential root causes.

### `custom_script_execution`

Execute a custom Python script for repository investigation or debugging. Use this when the required analysis cannot be performed using the standard repository search capabilities. The script can use the provided repository and file-system utilities to inspect files, search content, load modules, and perform custom analysis.

### `testing_changes`

Execute a custom Python script to test or validate changes made during repository investigation. Use this to run checks, inspect modified files, load relevant modules, or perform custom validation after making changes.
