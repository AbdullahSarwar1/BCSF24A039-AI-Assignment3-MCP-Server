# PUCIT CGPA Guider — Standalone MCP Server

This directory is a self-contained FastMCP server for the PUCIT BS(CS) academic tools. Publish the **contents of this directory** at the root of a dedicated GitHub repository if you want to deploy it independently.

## Tools exposed

The server exposes these eight plain Python functions as MCP tools:

1. `marks_to_grade_points`
2. `calculate_semester_gpa`
3. `calculate_new_cgpa`
4. `required_gpa_for_target`
5. `get_semester_courses`
6. `get_remaining_credit_hours`
7. `get_credit_hours`
8. `save_report`

FastMCP derives the tool schemas and descriptions from the functions' type hints and docstrings. This server folder intentionally does not require LangChain.

## Local run

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python server.py
```

The default endpoint is `http://127.0.0.1:8000/mcp`. Test from another terminal:

```bash
fastmcp list http://127.0.0.1:8000/mcp
fastmcp call http://127.0.0.1:8000/mcp get_credit_hours semesters='[5,6]' --auth none
```

The combined credit-hours result for semesters 5 and 6 should be `37.0`.

## Render deployment

The `render.yaml` file is intended to sit at the root of the GitHub repository connected to Render. The Blueprint installs this directory's `requirements.txt`, starts `python server.py`, and sets `HOST=0.0.0.0`. Render supplies `PORT`; `server.py` reads it.

After deployment, use the actual service URL provided by Render and append `/mcp`. The included configuration does not enable authentication. For a host that requires authentication, configure that provider's authentication and use the corresponding FastMCP client configuration in the agent.

**Free-hosting caveat:** free web services can sleep after inactivity and have ephemeral local filesystems. Files saved by `save_report` on the server's local disk should not be treated as permanent storage.
