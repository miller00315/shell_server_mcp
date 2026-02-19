# Shell Server (MCP)

A simple [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) server that exposes a **terminal** tool so clients can run shell commands.

## Requirements

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

## Installation

```bash
# With uv (recommended)
uv sync

# Or with pip
pip install "mcp[cli]"
```

## Running the server

| Method | Command | Description |
|--------|---------|-------------|
| **Run (stdio)** | `make run` or `uv run mcp run server.py` | Start the server for use by an MCP client (e.g. Cursor, Claude Desktop). |
| **Dev / Inspector** | `make dev` or `uv run mcp dev server.py` | Start the server with MCP Inspector for testing and debugging. |

## Exposed tool

### `terminal`

Runs a shell command and returns combined stdout, stderr, and exit code.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `command` | string | Yes | The shell command to run (e.g. `ls -la`, `echo hello`). |
| `cwd` | string | No | Working directory. If omitted, uses the server’s current directory. |

**Return value:** A single string in the form:

```
<stdout>
---
<stderr>
---
exit_code: <int>
```

**Limits:** Commands are limited to 60 seconds; longer runs result in a timeout error.

## Connecting from a client

Configure your MCP client to run this server via stdio, for example:

- **Command:** `uv`
- **Args:** `run`, `mcp`, `run`, `server.py`
- **Cwd:** project root (where `pyproject.toml` and `server.py` live)

Or use `python -m mcp run server.py` if dependencies are installed in the active environment.

## Security

**Warning:** The terminal tool runs arbitrary shell commands. Use only in trusted environments and only with clients you control. Do not expose this server to untrusted users or networks.

## Makefile targets

Run `make` or `make help` to list available targets.

- `make install` — Install dependencies (uv sync).
- `make run` — Run the MCP server (stdio).
- `make dev` — Run the server with MCP Inspector.
- `make help` — Show this help.
