import json
import os
from pathlib import Path
import runpy
import subprocess
import sys
from unittest.mock import Mock


ROOT = Path(__file__).resolve().parents[1]


def run_hook(command, tmp_path):
    guard = tmp_path / "sitecustomize.py"
    guard.write_text(
        "import sys\n"
        "def block(event, args):\n"
        "    if event in ('socket.connect', 'socket.getaddrinfo', 'urllib.Request'):\n"
        "        raise RuntimeError('Network forbidden in hook test: ' + event)\n"
        "sys.addaudithook(block)\n"
    )
    result = subprocess.run(
        command,
        shell=True,
        cwd=ROOT,
        env={
            "PATH": os.pathsep.join([str(Path(sys.executable).parent), "/usr/bin", "/bin"]),
            "HOME": str(tmp_path),
            "PYTHONPATH": str(tmp_path),
            "PYTHONDONTWRITEBYTECODE": "1",
        },
        capture_output=True,
        text=True,
        timeout=15,
    )
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


def get_hooks(tmp_path):
    command = json.loads((ROOT / "slack.json").read_text())["hooks"]["get-hooks"]
    return run_hook(command, tmp_path)


def test_configured_hook_discovery(tmp_path):
    payload = get_hooks(tmp_path)
    assert {"start", "get-manifest"} <= payload["hooks"].keys()
    assert payload["config"]["sdk-managed-connection-enabled"] is True
    assert payload["runtime"] == "python"


def test_discovered_manifest_hook(tmp_path):
    hooks = get_hooks(tmp_path)["hooks"]
    assert run_hook(hooks["get-manifest"], tmp_path) == json.loads((ROOT / "manifest.json").read_text())


def test_default_start_hook_reaches_registered_app(monkeypatch):
    from slack_bolt.adapter.socket_mode import SocketModeHandler
    from slack_sdk import WebClient

    auth_test = Mock(return_value={"ok": True, "user_id": "U_APP", "bot_id": "B_APP", "team_id": "T_TEST"})
    started = []
    monkeypatch.setattr(WebClient, "auth_test", auth_test)
    monkeypatch.setattr(SocketModeHandler, "start", lambda handler: started.append(handler))
    monkeypatch.setenv("SLACK_BOT_TOKEN", "xoxb-test-only")
    monkeypatch.setenv("SLACK_APP_TOKEN", "xapp-test-only")
    monkeypatch.setenv("SLACK_SIGNING_SECRET", "signing-test-only")
    monkeypatch.delenv("SLACK_APP_PATH", raising=False)
    monkeypatch.setattr(sys, "argv", ["slack_cli_hooks.hooks.start"])
    monkeypatch.chdir(ROOT)

    runpy.run_module("slack_cli_hooks.hooks.start", run_name="__main__")

    auth_test.assert_called_once()
    assert len(started) == 1
    assert len(started[0].app._listeners) == 5
