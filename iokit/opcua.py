"""Local asyncua server that publishes the SIMULATED rack, plus a thin client.

The server holds the controller process image. `scan()` plays the role of one controller
cycle: copy output commands written by clients to the rack, then refresh all input nodes.
"""

from __future__ import annotations

import logging
import socket

from asyncua import Client, Server, ua

from .iolist import IOList
from .rack import FieldRack

NAMESPACE = "urn:iokit:sim-rack"
logging.getLogger("asyncua").setLevel(logging.ERROR)


def free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class RackServer:
    def __init__(self, iol: IOList, rack: FieldRack, port: int | None = None):
        self.iol = iol
        self.rack = rack
        self.url = f"opc.tcp://127.0.0.1:{port or free_port()}/iokit/"
        self.server = Server()
        self.inputs: dict[str, tuple] = {}
        self.outputs: dict = {}

    async def __aenter__(self) -> RackServer:
        await self.server.init()
        self.server.set_endpoint(self.url)
        self.server.set_server_name("iokit simulated rack A1")
        self.server.set_security_policy([ua.SecurityPolicyType.NoSecurity])
        idx = await self.server.register_namespace(NAMESPACE)
        rack_obj = await self.server.nodes.objects.add_object(idx, "SimRackA1")
        for p in self.iol.points:
            if p.signal == "DO":
                node = await rack_obj.add_variable(ua.NodeId(p.tag, idx), p.tag, False,
                                                   varianttype=ua.VariantType.Boolean)
                await node.set_writable()
                self.outputs[p.tag] = node
                continue
            vt = ua.VariantType.Boolean if p.signal == "DI" else ua.VariantType.Double
            init = False if p.signal == "DI" else 0.0
            self.inputs[p.tag] = (
                await rack_obj.add_variable(ua.NodeId(p.tag, idx), p.tag, init, varianttype=vt),
                await rack_obj.add_variable(ua.NodeId(f"{p.tag}.raw", idx), f"{p.tag}.raw", init,
                                            varianttype=vt),
                await rack_obj.add_variable(ua.NodeId(f"{p.tag}.status", idx), f"{p.tag}.status",
                                            "OK", varianttype=ua.VariantType.String),
            )
        await self.server.start()
        await self.scan()
        return self

    async def __aexit__(self, *exc) -> None:
        await self.server.stop()

    async def scan(self) -> None:
        srv = self.server
        for tag, node in self.outputs.items():
            self.rack.commands[tag] = bool(await node.read_value())
        for tag, (eng_n, raw_n, st_n) in self.inputs.items():
            raw, eng, status = self.rack.read_channel(tag)
            vt = ua.VariantType.Boolean if isinstance(raw, bool) else ua.VariantType.Double
            await srv.write_attribute_value(eng_n.nodeid, ua.DataValue(ua.Variant(eng, vt)))
            await srv.write_attribute_value(raw_n.nodeid, ua.DataValue(ua.Variant(raw, vt)))
            await srv.write_attribute_value(
                st_n.nodeid, ua.DataValue(ua.Variant(status, ua.VariantType.String)))


class RackClient:
    """OPC UA client used by the loop-check runner (a separate TCP connection)."""

    def __init__(self, url: str, iol: IOList):
        self.client = Client(url, timeout=10)
        self.iol = iol
        self.inputs = [p.tag for p in iol.points if p.signal != "DO"]

    async def __aenter__(self) -> RackClient:
        await self.client.connect()
        idx = await self.client.get_namespace_index(NAMESPACE)
        get = self.client.get_node
        self.nodes = []
        for t in self.inputs:
            self.nodes += [get(ua.NodeId(t, idx)), get(ua.NodeId(f"{t}.raw", idx)),
                           get(ua.NodeId(f"{t}.status", idx))]
        self.cmd = {p.tag: get(ua.NodeId(p.tag, idx)) for p in self.iol.points if p.signal == "DO"}
        return self

    async def __aexit__(self, *exc) -> None:
        await self.client.disconnect()

    async def read_inputs(self) -> dict[str, tuple]:
        """One batched read of every input: tag -> (raw, eng, status)."""
        vals = await self.client.read_values(self.nodes)
        return {t: (vals[3 * i + 1], vals[3 * i], vals[3 * i + 2]) for i, t in enumerate(self.inputs)}

    async def write_command(self, tag: str, value: bool) -> None:
        await self.cmd[tag].write_value(ua.DataValue(ua.Variant(bool(value), ua.VariantType.Boolean)))
