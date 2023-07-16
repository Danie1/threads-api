class HTTPSession:
    async def start(self):
        raise NotImplementedError

    def auth(self, auth_callback_func, **kwargs):
        raise NotImplementedError

    async def close(self):
        raise NotImplementedError

    async def post(self, **kwargs):
        raise NotImplementedError

    async def get(self, **kwargs):
        raise NotImplementedError