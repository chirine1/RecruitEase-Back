from uvicorn import run


from src.config.settings import Settings

if __name__ == "__main__":
    
        run(
            "src.api:app",
            host="localhost",
            port=Settings().PORT,
            reload=True,
        )
