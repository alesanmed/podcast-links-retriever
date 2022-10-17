class PodcastNotFoundError(Exception):
    def __init__(self, show_id: str):
        self.show_id = show_id
        self.message = "Show not found"

        super().__init__(self.message)

    def __str__(self) -> str:
        return f"{self.message} Show ID: {self.show_id}"
