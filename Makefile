.PHONY: help install run dev

help:
	@echo "Shell Server (MCP) - targets:"
	@echo "  make install  Install dependencies (uv sync)"
	@echo "  make run      Run the MCP server (stdio)"
	@echo "  make dev      Run the server with MCP Inspector"
	@echo "  make help     Show this help"

install:
	uv sync

run:
	uv run mcp run server.py

dev:
	uv run mcp dev server.py
