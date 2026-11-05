import math

SYMBOLS={
 "R_10":"Volatility 10 Index",
 "R_25":"Volatility 25 Index",
 "R_50":"Volatility 50 Index",
 "R_75":"Volatility 75 Index",
 "R_100":"Volatility 100 Index",
 "1HZ10V":"Volatility 10 (1s) Index",
 "1HZ25V":"Volatility 25 (1s) Index",
 "1HZ50V":"Volatility 50 (1s) Index",
 "1HZ75V":"Volatility 75 (1s) Index",
 "1HZ100V":"Volatility 100 (1s) Index",
}

def rsi(values,period=14):
    if len(values)<period+1: return 50.0
    changes=[values[i]-values[i-1] for i in range(1,len(values))]
    gains=[max(x,0) for x in changes[-period:]]
    losses=[max(-x,0) for x in changes[-period:]]
    avg_gain=sum(gains)/period
    avg_loss=sum(losses)/period
    if avg_loss==0: return 100.0 if avg_gain else 50.0
    return 100-(100/(1+avg_gain/avg_loss))

def analyze_ticks(symbol,prices):
    if len(prices)<40: raise ValueError(f"Poucos ticks para {symbol}")
    p=list(map(float,prices))
    last=p[-1]
    short=sum(p[-8:])/8
    long=sum(p[-30:])/30
    mom=p[-1]-p[-11]
    vol=sum(abs(p[i]-p[i-1]) for i in range(-20,-1))/19
    strength=abs(mom)/(vol*10+1e-12)
    r=rsi(p)
    score=0
    score += 1 if short>long else -1
    score += 1 if mom>0 else -1
    score += 1 if r>53 else -1 if r<47 else 0
    if score>=2:
        signal="RISE"
    elif score<=-2:
        signal="FALL"
    else:
        signal="WAIT"
    confidence=min(85,round(50+min(25,strength*5)+abs(score)*3)) if signal!="WAIT" else 50
    reason=f"EMA/SMA proxy curto vs longo; momentum de 10 ticks {'positivo' if mom>0 else 'negativo'}; RSI {r:.1f}. Regra técnica simples, não validada como previsão."
    return {"name":SYMBOLS.get(symbol,symbol),"symbol":symbol,"signal":signal,"entry":"Próximo tick (somente alerta)" if signal!="WAIT" else "Aguardar","confidence":confidence,"rsi":r,"momentum":round(mom,6),"reason":reason,"prices":p[-100:]}
