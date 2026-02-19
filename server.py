"""
Simple MCP server that exposes a terminal tool to run shell commands.

WARNING: This tool executes arbitrary commands. Use only in trusted 
environments.
"""

import asyncio
import logging
from mcp.server.fastmcp import FastMCP

# MCP STDIO servers must not write to stdout; use stderr for logs.
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
    stream=__import__("sys").stderr,
)
logger = logging.getLogger(__name__)

mcp = FastMCP("Shell Server")


@mcp.tool()
async def terminal(command: str, cwd: str | None = None) -> str:
    """Run a shell command and return its output.

    Executes the given command asynchronously in the default shell (sh). Use
    only in trusted environments; this tool can run arbitrary commands.

    Args:
        command: The shell command to run (e.g. "ls -la", "echo hello").
        cwd: Optional working directory. If not set, uses the server's
            current directory.

    Returns:
        A string with stdout and stderr combined; includes exit code on the 
        last line.
        Format: "stdout\\n---\\nstderr\\n---\\nexit_code: <int>"
    """
    if not command or not command.strip():
        return "error: command cannot be empty\n---\n---\nexit_code: -1"

    try:
        proc = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=cwd or None,
        )
        try:
            stdout_bytes, stderr_bytes = await asyncio.wait_for(
                proc.communicate(), timeout=60
            )
        except asyncio.TimeoutError:
            proc.kill()
            await proc.wait()
            logger.warning("terminal tool: command=%r timed out", command)
            return (
                "error: command timed out after 60s\n---\n---\nexit_code: -1"
            )
        stdout = (stdout_bytes or b"").decode(errors="replace")
        stderr = (stderr_bytes or b"").decode(errors="replace")
        exit_code = proc.returncode or 0
        logger.info(
            "terminal tool: command=%r exit_code=%s", command, exit_code
        )
        return f"{stdout}\n---\n{stderr}\n---\nexit_code: {exit_code}"
    except Exception as e:
        logger.exception("terminal tool failed: command=%r", command)
        return f"error: {e!s}\n---\n---\nexit_code: -1"


if __name__ == "__main__":
    mcp.run()
