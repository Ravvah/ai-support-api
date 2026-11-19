import os

import uvicorn

if __name__ == "__main__":
    try:
        port = int(os.environ.get("PORT", "8000"))
    except ValueError:
        raise SystemExit("PORT need to be an integer") from None
    
    if not 1 <= port <= 65535:
        raise SystemExit("PORT need to be between 1 and 65535")
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)

