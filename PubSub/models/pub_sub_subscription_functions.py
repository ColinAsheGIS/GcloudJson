from httpx import AsyncClient

from .pub_sub_subscriptions import AckRequest

async def acknowledge(
        client: AsyncClient,
        subscription: str,
        ack_request: AckRequest
    ) -> None:
    res = await client.post(
        url=f"{subscription}:acknowledge",
        content=ack_request.json(by_alias=True)
    )
    if res.status_code != 200:
        raise Exception()
    return
