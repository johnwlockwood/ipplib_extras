from __future__ import print_function
import os

from pkipplib import pkipplib


def get_cups():
    """
    Get an authenticated cups instance.

    :return:
    """
    return pkipplib.CUPS(
        url="https://{}:{}".format(
            os.environ['CUPS_PORT_631_TCP_ADDR'],
            os.environ['CUPS_PORT_631_TCP_PORT']),
        username=os.environ["CUPS_ENV_CUPS_USER_ADMIN"],
        password=os.environ["CUPS_ENV_CUPS_USER_PASSWORD"])


def is_printer(printer_name, cups=None):
    """
    Determine if printer_name is an available printer.

    :param printer_name:
    :param cups:
    :return:
    """
    if not cups:
        cups = get_cups()

    printers = cups.getPrinters()
    if printer_name in printers:
        return True


def print_data(data, printer_name=None):
    """
    Send a print job of data to the cups server.

    :param data: bytes
    :return:
    """
    if not printer_name:
        printer_name = os.environ.get("CUPS_PRINTER", "HPLaserJet4000")

    cups = get_cups()
    request = cups.newRequest(pkipplib.IPP_PRINT_JOB)
    request.data = data
    request.operation["printer-uri"] = (
        "uri", "https://localhost:631/printers/{}".format(printer_name))
    return cups.doRequest(request)


if __name__ == "__main__":
    answer = print_data("hello world")
    print(answer)
