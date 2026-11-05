import json, websocket

class DerivClient:
    def __init__(self, app_id):
        self.url=f"wss://ws.derivws.com/websockets/v3?app_id={app_id}"
    def get_ticks(self, symbol, count=300):
        ws=websocket.create_connection(self.url,timeout=20)
        try:
            ws.send(json.dumps({"ticks_history":symbol,"count":count,"end":"latest","style":"ticks"}))
            while True:
                msg=json.loads(ws.recv())
                if "error" in msg: raise RuntimeError(msg["error"].get("message","Deriv API error"))
                if msg.get("msg_type")=="history":
                    hist=msg.get("history",{})
                    prices=[float(x) for x in hist.get(" prices",hist.get("prices",[]))]
                    if not prices: raise RuntimeError("A API não devolveu preços.")
                    return prices
        finally:
            ws.close()
