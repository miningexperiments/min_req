# Run
```sh
pip install speedtest-cli psutil 
python minrequirements.py
```
## Common errors:
```sh
Initializing speed test...
❌ Error: HTTP Error 403: Forbidden
```
This is due to speedtest servers spam protection. Usually means you are behind an IP that has frequently tested speed and now being throttled by Ookla.
