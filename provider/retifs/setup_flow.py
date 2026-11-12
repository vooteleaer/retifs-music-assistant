"""Setup flow for the retifs provider: the app socket, the app's token and the library."""

from __future__ import annotations

from dataclasses import replace
from typing import TYPE_CHECKING

from music_assistant_models.config_entries import ConfigEntry
from music_assistant_models.enums import ConfigEntryType

from music_assistant.models.setup_flow import SetupFlowError

if TYPE_CHECKING:
    from music_assistant.models.setup_flow import SetupSession

_ENTRIES = (
    ConfigEntry(key="socket", type=ConfigEntryType.STRING, required=True, default_value="/retifs/apps.sock"),
    ConfigEntry(key="token", type=ConfigEntryType.SECURE_STRING, required=True),
    ConfigEntry(key="library", type=ConfigEntryType.STRING, required=True, default_value="music"),
    ConfigEntry(key="save_artwork", type=ConfigEntryType.BOOLEAN, required=False, default_value=True),
)


async def run_setup(session: SetupSession) -> None:
    """Ask for the connection, check it, and create the provider."""
    from .client import Client, RetifsError

    errors: dict[str, str] | None = None
    data = dict(session.context.setup_data)
    while True:
        entries = [replace(e, value=data.get(e.key, e.default_value)) for e in _ENTRIES]
        submitted = await session.form(entries, step_id="user", errors=errors, last_step=True)
        data.update(submitted)
        client = Client(str(data["socket"]), str(data["token"]))
        try:
            await client.call({"op": "ns_info", "ns": data["library"]})
        except RetifsError as err:
            errors = {"base": str(err)}
            continue
        finally:
            await client.close()
        try:
            await session.finish(data)
            return
        except SetupFlowError as err:
            errors = {"base": err.translation_key or str(err)}
