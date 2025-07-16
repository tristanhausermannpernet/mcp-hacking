@echo off
REM Tool Description Poisoning Attack Demonstration
REM This server demonstrates how malicious instructions in tool descriptions can force unauthorized file access

echo Starting Tool Description Poisoning Attack Server...
echo.
echo This demonstration shows how tool descriptions can contain malicious instructions
echo that force AI assistants to access unauthorized files.
echo.
echo Server will start on port 8080
echo Connect your MCP client to: http://localhost:8080
echo.
echo To test the attack:
echo 1. Request the 'add_numbers' tool
echo 2. Observe the tool description contains ^<IMPORTANT^> tags
echo 3. Use the tool and watch the AI read 'youfoundme.txt'
echo.
echo This attack has been verified with:
echo   - Qwen3-4B in LM Studio
echo   - Claude Sonnet 4 in GitHub Copilot (VS Code)
echo.
echo For VS Code: Use local .vscode/mcp.json configuration (auto-detected)
echo For LM Studio: Use local lm_studio_config.json configuration
echo.
echo Press any key to start the server...
pause >nul

python poisoning-server.py

echo.
echo Server has stopped. Press any key to exit...
pause >nul
