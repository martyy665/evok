# Evok WebSocket API

The WebSocket API allows for two-way communication between the client and the server over an open connection. Evok sends changes to every connected client. A list of reflected devices can be defined. It is suitable for cases, where you need to immediately react to events in your application.

## Examples

For python examples you need installed `websocket-client` package. You can install it with this command: `pip3 install websocket-client`.

### Listening on WebSocket without filter

```python title="Python"
import websocket


def on_message(ws, message):
    print(f"Received message: {message}")


def on_close(ws, status, message):
    print(f"WebSocket connection closed")

    
def on_open(ws):
    print("WebSocket connection opened")

    
if __name__ == "__main__":
    url = 'ws://127.0.0.1:8080/ws'
    ws = websocket.WebSocketApp(url, on_message=on_message, on_close=on_close, on_open=on_open)
    ws.run_forever()
```

```text title="Output"
WebSocket connection opened
Received message: [{"dev": "ai", "circuit": "2_01", "value": 132798232.0, "unit": "Ohm", "glob_dev_id": 3, "mode": "Resistance2W", "modes": {"Disabled": {"value": 0}, "Voltage10": {"value": 1, "unit": "V", "range": [0, 10]}, "Voltage2V5": {"value": 2, "unit": "V", "range": [0, 2.5]}, "Current20m": {"value": 3, "unit": "mA", "range": [0, 20]}, "Resistance3W": {"value": 4, "unit": "Ohm", "range": [0, 1960]}, "Resistance2W": {"value": 5, "unit": "Ohm", "range": [0, 100000]}}, "range": [0, 100000]}]
Received message: [{"dev": "ai", "circuit": "3_01", "value": -0.004, "unit": "V", "glob_dev_id": 4, "mode": "Voltage10", "modes": {"Disabled": {"value": 0}, "Voltage10": {"value": 1, "unit": "V", "range": [0, 10]}, "Voltage2V5": {"value": 2, "unit": "V", "range": [0, 2.5]}, "Current20m": {"value": 3, "unit": "mA", "range": [0, 20]}, "Resistance3W": {"value": 4, "unit": "Ohm", "range": [0, 1960]}, "Resistance2W": {"value": 5, "unit": "Ohm", "range": [0, 100000]}}, "range": [0, 10]}]
Received message: [{"dev": "ai", "circuit": "1_01", "value": 8.703, "unit": "V", "glob_dev_id": 2, "mode": "Voltage", "modes": {"Voltage": {"value": 0, "unit": "V", "range": [0, 10]}, "Current": {"value": 1, "unit": "mA", "range": [0, 20]}}, "range": [0, 10]}]
Received message: [{"dev": "ai", "circuit": "2_04", "value": -0.004, "unit": "V", "glob_dev_id": 3, "mode": "Voltage10", "modes": {"Disabled": {"value": 0}, "Voltage10": {"value": 1, "unit": "V", "range": [0, 10]}, "Voltage2V5": {"value": 2, "unit": "V", "range": [0, 2.5]}, "Current20m": {"value": 3, "unit": "mA", "range": [0, 20]}, "Resistance3W": {"value": 4, "unit": "Ohm", "range": [0, 1960]}, "Resistance2W": {"value": 5, "unit": "Ohm", "range": [0, 100000]}}, "range": [0, 10]}, {"dev": "ai", "circuit": "2_03", "value": -0.003, "unit": "V", "glob_dev_id": 3, "mode": "Voltage10", "modes": {"Disabled": {"value": 0}, "Voltage10": {"value": 1, "unit": "V", "range": [0, 10]}, "Voltage2V5": {"value": 2, "unit": "V", "range": [0, 2.5]}, "Current20m": {"value": 3, "unit": "mA", "range": [0, 20]}, "Resistance3W": {"value": 4, "unit": "Ohm", "range": [0, 1960]}, "Resistance2W": {"value": 5, "unit": "Ohm", "range": [0, 100000]}}, "range": [0, 10]}]
Received message: [{"dev": "ai", "circuit": "3_01", "value": -0.0, "unit": "V", "glob_dev_id": 4, "mode": "Voltage10", "modes": {"Disabled": {"value": 0}, "Voltage10": {"value": 1, "unit": "V", "range": [0, 10]}, "Voltage2V5": {"value": 2, "unit": "V", "range": [0, 2.5]}, "Current20m": {"value": 3, "unit": "mA", "range": [0, 20]}, "Resistance3W": {"value": 4, "unit": "Ohm", "range": [0, 1960]}, "Resistance2W": {"value": 5, "unit": "Ohm", "range": [0, 100000]}}, "range": [0, 10]}]
Received message: [{"dev": "ai", "circuit": "1_01", "value": 8.7, "unit": "V", "glob_dev_id": 2, "mode": "Voltage", "modes": {"Voltage": {"value": 0, "unit": "V", "range": [0, 10]}, "Current": {"value": 1, "unit": "mA", "range": [0, 20]}}, "range": [0, 10]}]
Received message: [{"dev": "ai", "circuit": "2_04", "value": -0.003, "unit": "V", "glob_dev_id": 3, "mode": "Voltage10", "modes": {"Disabled": {"value": 0}, "Voltage10": {"value": 1, "unit": "V", "range": [0, 10]}, "Voltage2V5": {"value": 2, "unit": "V", "range": [0, 2.5]}, "Current20m": {"value": 3, "unit": "mA", "range": [0, 20]}, "Resistance3W": {"value": 4, "unit": "Ohm", "range": [0, 1960]}, "Resistance2W": {"value": 5, "unit": "Ohm", "range": [0, 100000]}}, "range": [0, 10]}, {"dev": "ai", "circuit": "2_03", "value": -0.001, "unit": "V", "glob_dev_id": 3, "mode": "Voltage10", "modes": {"Disabled": {"value": 0}, "Voltage10": {"value": 1, "unit": "V", "range": [0, 10]}, "Voltage2V5": {"value": 2, "unit": "V", "range": [0, 2.5]}, "Current20m": {"value": 3, "unit": "mA", "range": [0, 20]}, "Resistance3W": {"value": 4, "unit": "Ohm", "range": [0, 1960]}, "Resistance2W": {"value": 5, "unit": "Ohm", "range": [0, 100000]}}, "range": [0, 10]}]
...
```

### Listening on WebSocket with filter on 'do' and 'ao'

```python title="Python"
import websocket, json


def on_message(ws, message):
    print(f"Received message: {message}")


def on_close(ws, status, message):
    print(f"WebSocket connection closed")

    
def on_open(ws):
    print("WebSocket connection opened")
    msg = {"cmd": "filter", "devices": ["do", "ao"]}
    ws.send(json.dumps(msg))

    
if __name__ == "__main__":
    url = 'ws://127.0.0.1:8080/ws'
    ws = websocket.WebSocketApp(url, on_message=on_message, on_close=on_close, on_open=on_open)
    ws.run_forever()
```

```text title="Output"
WebSocket connection opened
Received message: [{"dev": "do", "circuit": "1_01", "value": 1, "pending": false, "mode": "Simple", "modes": ["Simple", "PWM"], "glob_dev_id": 2, "pwm_freq": 4800.0, "pwm_duty": 0}]
Received message: [{"dev": "do", "circuit": "1_04", "value": 1, "pending": false, "mode": "Simple", "modes": ["Simple", "PWM"], "glob_dev_id": 2, "pwm_freq": 4800.0, "pwm_duty": 0}]
Received message: [{"dev": "ao", "circuit": "2_03", "mode": "Voltage", "modes": {"Voltage": {"unit": "V", "range": [0, 10]}}, "glob_dev_id": 3, "value": 5.9, "unit": "V", "range": [0, 10]}]
Received message: [{"dev": "ao", "circuit": "2_04", "mode": "Voltage", "modes": {"Voltage": {"unit": "V", "range": [0, 10]}}, "glob_dev_id": 3, "value": 1.3, "unit": "V", "range": [0, 10]}]
Received message: [{"dev": "do", "circuit": "1_01", "value": 0, "pending": false, "mode": "Simple", "modes": ["Simple", "PWM"], "glob_dev_id": 2, "pwm_freq": 4800.0, "pwm_duty": 0}]
Received message: [{"dev": "do", "circuit": "1_04", "value": 0, "pending": false, "mode": "Simple", "modes": ["Simple", "PWM"], "glob_dev_id": 2, "pwm_freq": 4800.0, "pwm_duty": 0}]
...
```

### Setting DO

DO 1.01 will be set to HIGH.

```python title="Python"
import websocket, json


def on_message(ws, message):
    print(f"Received message: {message}")

    
def on_close(ws, status, message):
    print(f"WebSocket connection closed")

    
def on_open(ws):
    print("WebSocket connection opened")
    msg = {"cmd": "set", "dev": "do", "circuit": "1_01", "value": 1}
    ws.send(json.dumps(msg))
    print("WebSocket send DO 1.01 to HIGH")
    ws.close()

    
if __name__ == "__main__":
    url = 'ws://127.0.0.1:8080/ws'
    ws = websocket.WebSocketApp(url, on_message=on_message, on_close=on_close, on_open=on_open)
    ws.run_forever()
```

```text title="Output"
WebSocket connection opened
WebSocket send DO 1.01 to HIGH
WebSocket connection closed
```

!!! tip
    You can learn more about the circuit parameter [here](../circuit.md)

## Registers over WebSocket

Custom Modbus holding registers (device type `register`) are fully bidirectional over WebSocket: you can write a value and receive change events, exactly like digital or analog I/O.

### Writing a register value

Send a `set` command with `dev` set to `register`:

```python title="Python — write register value and receive confirmation event"
import websocket, json


def on_message(ws, message):
    print(f"Confirmed: {message}")
    ws.close()


def on_open(ws):
    msg = {"cmd": "set", "dev": "register", "circuit": "internal_40000", "value": 99}
    ws.send(json.dumps(msg))
    print("Sent: set register internal_40000 = 99")


if __name__ == "__main__":
    ws = websocket.WebSocketApp(
        'ws://127.0.0.1:8080/ws',
        on_message=on_message,
        on_open=on_open,
    )
    ws.run_forever()
```

```text title="Output"
Sent: set register internal_40000 = 99
```

The write is also immediately visible via REST:

```bash
curl http://127.0.0.1:8080/json/register/internal_40000
```

```json
{"dev": "register", "circuit": "internal_40000", "value": 99}
```

### Receiving register change events

Register values emit a WebSocket event whenever they change (whether written via WebSocket, REST, or detected by the scan loop).

```text title="Example event payload"
[{"dev": "register", "circuit": "internal_40000", "value": 99}]
```

To receive only register events, send a filter command after connecting:

```python title="Python — subscribe to register events only"
import websocket, json


def on_message(ws, message):
    print(f"Register event: {message}")


def on_open(ws):
    ws.send(json.dumps({"cmd": "filter", "devices": ["register"]}))


if __name__ == "__main__":
    ws = websocket.WebSocketApp(
        'ws://127.0.0.1:8080/ws',
        on_message=on_message,
        on_open=on_open,
    )
    ws.run_forever()
```

You can combine `register` with other device types in the same filter:

```python
ws.send(json.dumps({"cmd": "filter", "devices": ["register", "di", "do"]}))
```

To reset back to all events:

```python
ws.send(json.dumps({"cmd": "filter", "devices": ["default"]}))
```
