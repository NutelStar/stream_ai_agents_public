# Stream AI Agents

A voice-driven AI assistant for live streams. It listens to a microphone, generates
a response with OpenAI, speaks it with ElevenLabs, and can display the avatar and
subtitles through OBS WebSocket.

## Requirements

- Python 3.9.2 or newer
- [Poetry](https://python-poetry.org/)
- OBS Studio with the WebSocket server enabled (optional; omit it with `--no-obs`)
- API credentials for OpenAI, Azure Speech, and ElevenLabs

## Setup

Fill in the environment variables and OBS connection settings:

| Variable | Description |
| --- | --- |
| `OPENAI_API_KEY` | OpenAI API key |
| `AZURE_TTS_KEY` | Azure Speech resource key |
| `AZURE_TTS_REGION` | Azure Speech resource region |
| `ELEVENLABS_API_KEY` | ElevenLabs API key |
| `OBS_WEBSOCKET_HOST` | OBS WebSocket host (default: `localhost`) |
| `OBS_WEBSOCKET_PORT` | OBS WebSocket port (default: `4455`) |
| `OBS_WEBSOCKET_PASSWORD` | OBS WebSocket password (empty if authentication is disabled) |

Runtime names and audio settings are centralized in
[`src/ai_agents/config.py`](src/ai_agents/config.py).

Then, you can start the assistant:

```powershell
poetry run python -m ai_agents
```

Run with OBS by adding `-obs`:

```powershell
poetry run python -m ai_agents -obs
```

The `run.bat` script provides the same launch command on Windows and forwards
arguments, so `run.bat -obs` works too.

## License

MIT License

Copyright (c) 2024 DougDougGithub

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
