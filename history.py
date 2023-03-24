class History:
    def __init__(self, user_id, name, url, res) -> None:
        self.tg_id: str = user_id
        self.name: str = name
        self.original_link: str = url
        self.result_link: str = res
