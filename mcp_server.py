import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Omniomicon")

VECTOR_API_BASE: str = "http://127.0.0.1"


async def create_note_request(text: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{VECTOR_API_BASE}/notes/", json={"text": text})
        response.raise_for_status()
        return response.json()


async def search_notes_request(query: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{VECTOR_API_BASE}/notes/search", json={"query": query}
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def create_note(text: str) -> str:
    await create_note_request(text)
    return "Note saved!"


@mcp.tool()
async def search_notes(question: str) -> str:
    notes = await search_notes_request(question)
    print(notes)
    return "\n ----- \n".join(note["text"] for note in notes)


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
