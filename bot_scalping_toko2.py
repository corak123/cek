import streamlit as st
import ccxt
import pandas as pd

st.title("Cek Data OHLCV dari Exchange")

# Input user
base = st.text_input("Base Currency", value="BTC")
quote = st.text_input("Quote Currency", value="USDT")
exchange_name = st.selectbox("Pilih Exchange", ['indodax', 'tokocrypto'])
timeframe = st.selectbox("Timeframe", ['1m', '5m', '15m', '1h', '1d'], index=3)
limit = st.slider("Limit Data", min_value=10, max_value=500, value=100)

# Tombol untuk cek data
if st.button("Ambil Data OHLCV"):
    # Fungsi untuk format pair
    def get_pair(base, quote, exchange_name):
        if exchange_name == 'indodax':
            return f"{base.lower()}_{quote.lower()}"
        elif exchange_name == 'tokocrypto':
            return f"{base.upper()}/{quote.upper()}"
        else:
            raise ValueError("Exchange tidak dikenali")

    try:
        pair = get_pair(base, quote, exchange_name)

        # Inisialisasi exchange
        exchange = getattr(ccxt, exchange_name)()

        # Ambil data
        with st.spinner("Mengambil data..."):
            ohlcv = exchange.fetch_ohlcv(pair, timeframe=timeframe, limit=limit)

        if not ohlcv:
            st.error("❌ Data OHLCV kosong!")
        else:
            df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
            st.success(f"✅ Berhasil mengambil {len(df)} data OHLCV!")
            st.dataframe(df)

    except Exception as e:
        st.error(f"❌ Gagal mengambil data: {e}")
