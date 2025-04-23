import os, sys
import streamlit.web.cli as stcli

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8501))
    sys.argv = [
      "streamlit", "run", "app_streamlit.py",
      "--server.port", str(port),
      "--server.address", "0.0.0.0",
    ]
    sys.exit(stcli.main())
