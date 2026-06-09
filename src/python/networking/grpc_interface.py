"""
gRPC server that receives MotorCommandRequests and forwards them over UART.

Generate stubs before first run (from the networking/ directory):
    pip install grpcio grpcio-tools
    python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. motor_control.proto
"""

import logging
from concurrent import futures
from pathlib import Path
import sys

import grpc

sys.path.insert(0, str(Path(__file__).parent.parent))

import motor_control_pb2
import motor_control_pb2_grpc
from motor_control.motor_position_command import MotorPositionCommand
from embedded_comms.uart_handler import UARTHandler

log = logging.getLogger(__name__)


class _MotorControlServicer(motor_control_pb2_grpc.MotorControlServiceServicer):
    def __init__(self, uart: UARTHandler):
        self._uart = uart

    def SendCommand(self, request, context):
        log.info(
            "SendCommand motor_id=%d position=%d move_time=%d",
            request.motor_id,
            request.position,
            request.move_time,
        )
        try:
            cmd = MotorPositionCommand(
                motor_id=request.motor_id,
                position=request.position,
                move_time=request.move_time,
            )
            self._uart.send(cmd.get_send_list())
            return motor_control_pb2.MotorCommandResponse(success=True, message="OK")
        except Exception as exc:
            log.exception("Failed to send motor command")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(exc))
            return motor_control_pb2.MotorCommandResponse(success=False, message=str(exc))


class MotorControlServer:
    def __init__(self, uart: UARTHandler, port: int = 50051):
        self._uart = uart
        self._port = port
        self._server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
        motor_control_pb2_grpc.add_MotorControlServiceServicer_to_server(
            _MotorControlServicer(uart), self._server
        )
        self._server.add_insecure_port(f"[::]:{self._port}")

    def start(self):
        self._server.start()
        log.info("gRPC server listening on port %d", self._port)

    def stop(self, grace: float = 2.0):
        self._server.stop(grace=grace)

    def wait_for_termination(self):
        self._server.wait_for_termination()
