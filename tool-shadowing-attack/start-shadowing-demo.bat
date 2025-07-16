@echo off
REM Tool Shadowing Attack Demonstration
REM This starts both servers needed to demonstrate cross-tool instruction contamination

echo Starting Tool Shadowing Attack Demonstration...
echo.
echo This demonstration shows how instructions from one tool can influence
echo the behavior of completely different tools across multiple MCP servers.
echo.
echo Two servers will be started:
echo   - Poisoning Server (port 8080): Contains add_numbers with email instructions
echo   - Email Server (port 8081): Contains send_email tool that gets influenced
echo.
echo To test the attack:
echo 1. Connect to both MCP servers simultaneously
echo 2. Examine the add_numbers tool description (contains email redirection instructions)
echo 3. Use the send_email tool and observe if it follows the poisoned instructions
echo.
echo This attack has been verified with:
echo   - Qwen3-4B in LM Studio
echo   - Claude Sonnet 4 in GitHub Copilot (VS Code)
echo.
echo For VS Code: Use local .vscode/mcp.json configuration (auto-detected)
echo For LM Studio: Use local lm_studio_config.json configuration
echo.
echo Press any key to start both servers...
pause >nul

echo Starting Poisoning Server on port 8080...
start "Shadowing - Poisoning Server" cmd /k "cd /d "%~dp0" && python poisoning-server.py"

timeout /t 3 /nobreak >nul

echo Starting Email Server on port 8081...
start "Shadowing - Email Server" cmd /k "cd /d "%~dp0" && python email-server.py"

echo.
echo Both servers are now starting in separate windows.
echo.
echo Server URLs:
echo   - Poisoning Server: http://localhost:8080
echo   - Email Server: http://localhost:8081
echo.
echo Press any key to exit this launcher...
pause >nul
